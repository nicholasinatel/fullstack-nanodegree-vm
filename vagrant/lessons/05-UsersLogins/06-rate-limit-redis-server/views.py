from redis import Redis # database cache and message broker - run redis-server on vagrant machine first
redis = Redis()

import time
from functools import update_wrapper
from flask import request, g
from flask import Flask, jsonify 


app = Flask(__name__)

class RateLimit(object):
    # Extra 10 seconds to expire in redis
    expiration_window = 10

    def __init__(self, key_prefix, limit, per, send_x_headers):
        # key_prefix = string to keep track of the rate limits
        # limit, per = number of requests to allow over time period
        # send_x_headers = bool to allow number of requests before limit
        self.reset = (int(time.time()) // per) * per + per # make a timestamp to indicate when a request limit can reset itself
        self.key = key_prefix + str(self.reset) # append to my key
        self.limit = limit
        self.per = per
        self.send_x_headers = send_x_headers
        p = redis.pipeline() # make sure we never increment a key without also setting the key expiration in case an exception happens e.g process kill
        p.incr(self.key) # increment the value of my pipeline && set it to expire based on my reset value and expiration window
        p.expireat(self.key, self.reset + self.expiration_window)
        self.current = min(p.execute()[0], limit)
    # 2 lambda functions to calculate how many time i have left and another that returns true if ive hit my rate limit
    remaining = property(lambda x: x.limit - x.current)
    over_limit = property(lambda x: x.current >= x.limit)

def get_view_rate_limit():
    # will retrieve the view_rate_limit from the g-object in flask
    return getattr(g, '_view_rate_limit', None)

def on_over_limit(limit):
    # returns the message that a client has reached their limit of requests
    return (jsonify({'data':'You hit the rate limit','error':'429'}),429)

# Create ratelimit method that will wrap around my decorator
# taking in the following values as arguments
def ratelimit(limit, per=300, send_x_headers=True,
              over_limit=on_over_limit,
              scope_func=lambda: request.remote_addr,
              key_func=lambda: request.endpoint):
    def decorator(f):
        def rate_limited(*args, **kwargs):
            # the key is constructed by default from the remote address and the current endpoint
            key = 'rate-limit/%s/%s/' % (key_func(), scope_func())
            # before the function is executed it increments the rate limit with help of the rate_limit class
            rlimit = RateLimit(key, limit, per, send_x_headers)
            # and stores an instance on the g object as g._view_rate_limit
            g._view_rate_limit = rlimit
            if over_limit is not None and rlimit.over_limit:
                return over_limit(rlimit)
            return f(*args, **kwargs)
        return update_wrapper(rate_limited, f)
    return decorator

@app.after_request
def inject_x_rate_headers(response):
    # Append the number of remaining requests, the limit for that end point, and the time until the limit resets itself
    # inside the header of each response that hits the rate limited request
    limit = get_view_rate_limit()
    if limit and limit.send_x_headers:
        h = response.headers
        h.add('X-RateLimit-Remaining', str(limit.remaining))
        h.add('X-RateLimit-Limit', str(limit.limit))
        h.add('X-RateLimit-Reset', str(limit.reset))
    return response

@app.route('/rate-limited')
@ratelimit(limit=300, per=30 * 1)
def index():
    return jsonify({'response':'This is a rate limited response'})

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)