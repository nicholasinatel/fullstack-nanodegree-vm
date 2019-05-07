# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Category, Base, Item, Rentability, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create Guest User
User1 = User(name="Guest Investor",
             email="testerguest4myapp@gmail.com",
             picture=('https://lh6.googleusercontent.com/'
                      '-E7BpjMMXKvw/AAAAAAAAAAI/AAAAAAAAAAc/'
                      '_sYAZwlCY10/photo.jpg'))
session.add(User1)
session.commit()

# Carteira de Dividendos
category1 = Category(name="Dividendos",
                     description=('Forma de remuneração que as '
                                  'empresas fazem aos seus acionistas'
                                  ' de tempos'
                                  ' em tempos, '
                                  'feita em dinheiro e anunciada '
                                  'pelo conselho '
                                  'de administração. Os dividendos são, '
                                  'portanto, a parte que os investidores'
                                  ' têm dos'
                                  ' lucros da companhia, á'
                                  'uma vez que são sócios desta empresa.'),
                     user_id=1)
session.add(category1)
session.commit()

# Assets
# 1
item1 = Item(name="AES Tietê", active="TIET11", dy="8.1%", price="R$11,15",
             description=("AES Tietê é uma empresa de geração de energia"
                          " de elétrica pertencente ao grupo AES Brasil. "
                          "Possui ações preferenciais e ordinárias negociadas"
                          " na BM&FBovespa. "),
             category=category1,
             user_id=1)
session.add(item1)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item1, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='May', money=55.0,
                      percent=0.8, item=item1, user_id=1)
session.add(renDiv2)
session.commit()

# 2
item2 = Item(name="EDP Energias do Brasil SA",
             active="ENBR3",
             dy="3.6%",
             price="R$17,85",
             description=("A EDP Brasil é uma holding "
                          "brasileira do setor elétrico."
                          "Ela detém investimentos no "
                          "setor de energia, ativos de "
                          "geração,"
                          "comercialização e distribuição "
                          "em 11 estados: São Paulo,"
                          " Espírito Santo,"
                          "Minas Gerais, Mato Grosso do Sul, "
                          "Tocantins, Amapá, Pará,"
                          "Maranhão, Ceará, Santa Catarina "
                          "e Rio Grande do Sul."),
             category=category1, user_id=1)
session.add(item2)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item2, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='May', money=55.0,
                      percent=0.8, item=item2, user_id=1)
session.add(renDiv2)
session.commit()
# 3
item3 = Item(name="Tupy SA", active="TUPY3", dy="7.6%", price="R$18,12",
             description=("A Tupy é uma multinacional brasileira"
                          " do ramo da metalurgia "
                          "fundada em 9 de março de 1938 "
                          "na cidade de Joinville. "
                          "A companhia conta com cerca de 13 mil"
                          " funcionários em quatro parques fabris: "
                          "dois instalados no Brasil e dois no"
                          " estado de Coahuila, no México."),
             category=category1, user_id=1)
session.add(item3)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item3, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='May', money=55.0,
                      percent=0.8, item=item3, user_id=1)
session.add(renDiv2)
session.commit()

# 4
item4 = Item(name="Wiz Soluções", active="WIZS3", dy="12.7%", price="R$8,63",
             description=("Fazemos a distribuição de serviços"
                          " financeiros e de seguros "
                          "através da nossa plataforma multicanal."
                          " Transformamos dados em conhecimento "
                          "e conectamos pessoas a empresas, "
                          "oportunidades a necessidades, "
                          "para potencializar negócios. Ao longo dos "
                          "mais de 40 anos de atuação, "
                          "desenvolvemos e implementamos plataformas "
                          "integradas de relacionamento "
                          "e venda, garantindo agilidade e presença "
                          "em todo território nacional. "),
             category=category1, user_id=1)
session.add(item4)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item4, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='May', money=55.0,
                      percent=0.8, item=item4, user_id=1)
session.add(renDiv2)
session.commit()

# 5
item5 = Item(name="BB Seguridade", active="BBSE3", dy="6.0%", price="R$28,25",
             description=("BB Seguridade é uma empresa de "
                          "seguros brasileira pertencente "
                          "ao Banco do Brasil. A companhia foi "
                          "criada em 20 de dezembro de 2012 "
                          "após o Banco do Brasil separar a "
                          "sua divisão de seguros em uma "
                          "nova empresa de capital aberto "
                          "na BM&F Bovespa. "),
             category=category1, user_id=1)
session.add(item5)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item5, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='May', money=55.0,
                      percent=0.8, item=item5, user_id=1)
session.add(renDiv2)
session.commit()

# 6
item6 = Item(name="Banco ABC Brasil",
             active="ABCB4",
             dy="5.7%",
             price="R$19,33",
             description=("O Banco ABC BRASIL, controlado "
                          "pelo Arab Banking Corporation (ABC), "
                          "é um banco múltiplo, "
                          "especializado na concessão de"
                          " crédito e serviços para "
                          "empresas de médio a grande porte, "
                          "habilitado a"
                          " operar nas carteiras Comercial, "
                          "de Investimentos, Financeira, "
                          "Crédito Imobiliário e Câmbio. "),
             category=category1, user_id=1)
session.add(item6)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item6, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='May', money=55.0,
                      percent=0.8, item=item6, user_id=1)
session.add(renDiv2)
session.commit()

# 7
item7 = Item(name="Grendene", active="GRND3", dy="5.3%", price="R$8,44",
             description=("Grendene é uma empresa brasileira de fabricação"
                          " de calçados "
                          "cujo acionista majoritário é Alexandre Grendene"
                          " Bartelle e no ano de 2013 "
                          "foi a maior exportadora de calçados do Brasil. "
                          "Foi fundada em Farroupilha, no Rio Grande do Sul,"
                          " em 25 de fevereiro de 1971. "),
             category=category1, user_id=1)
session.add(item7)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item7, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='May', money=55.0,
                      percent=0.8, item=item7, user_id=1)
session.add(renDiv2)
session.commit()

# 8
item8 = Item(name="Taesa", active="TAEE11", dy="8.1%", price="R$25,90",
             description=("Transmissora Aliança "
                          "de Energia Elétrica SA ( TAESA ​), "
                          "empresa listada em bolsa, é um dos maiores"
                          " grupos privados de transmissão "
                          "de energia elétrica no Brasil, "
                          "exclusivamente"
                          " dedicada à construção, "
                          "operação e manutenção de "
                          "linhas de transmissão. "),
             category=category1, user_id=1)
session.add(item8)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item8, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='May', money=55.0,
                      percent=0.8, item=item8, user_id=1)
session.add(renDiv2)
session.commit()

# 9
item9 = Item(name="ItaúSA",
             active="ITSA4",
             dy="6.2%",
             price="R$12,06",
             description=("Itaúsa é uma holding "
                          "brasileira que controla "
                          "o Itaú Unibanco "
                          "(instituição financeira), "
                          "Duratex (papel e celulose),"
                          " Alpargatas (calçados), "
                          "Itautec (tecnologia da informação)"
                          " e participação na "
                          "NTS além de outros "
                          "empreendimentos."
                          " É o segundo maior"
                          " grupo privado do país. "),
             category=category1, user_id=1)
session.add(item9)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item9, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='May', money=55.0,
                      percent=0.8, item=item9, user_id=1)
session.add(renDiv2)
session.commit()

# 10
item10 = Item(name="Telefônica Vivo",
              active="VIVT4",
              dy="5.9%",
              price="R$50,02",
              description=("Telefônica Brasil é uma"
                           " empresa do Grupo Telefónica, "
                           "um dos principais conglomerados"
                           " de comunicação do mundo. "
                           "Foi originalmente formada a"
                           " partir da Telesp"
                           " (subsidiária da Telebrás), "
                           "companhia estatal de "
                           "telecomunicações que atuava "
                           "no estado de São Paulo "
                           "e que em 1998 foi privatizada"
                           " pelo governo"
                           " federal e vendida "
                           "para o Grupo Telefónica,"
                           " formando a Telefônica Brasil. "),
              category=category1, user_id=1)
session.add(item10)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item10, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='May', money=55.0,
                      percent=0.8, item=item10, user_id=1)
session.add(renDiv2)
session.commit()

# 11
item11 = Item(name="Unipar",
              active="UNIP6",
              dy="3.0%",
              price="R$38,77",
              description=("A Unipar Carbocloro é uma empresa química"
                           " brasileira de "
                           "capital aberto sediada em São Paulo"
                           " fabricante de cloro, "
                           "soda e derivados para usos industriais e "
                           "presidida desde 2015 por Anibal do Vale. "),
              category=category1, user_id=1)
session.add(item11)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item11, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='May', money=55.0,
                      percent=0.8, item=item11, user_id=1)
session.add(renDiv2)
session.commit()

# 12
item12 = Item(name="Multiplus",
              active="MPLU3",
              dy="9.9%",
              price="R$26,84",
              description=("A Multiplus é a rede de fidelidade líder e"
                           " pioneira do setor, "
                           "composta por 288 parceiros e mais de 21,6"
                           " milhões de participantes. "
                           "Ao conectar diferentes empresas e programas"
                           " de fidelidade, "
                           "a Multiplus permite aos seus participantes"
                           " acumularem pontos, "
                           "em uma única conta, em diversas atividades"
                           " do dia-a-dia. "),
              category=category1, user_id=1)
session.add(item12)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item12, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='May', money=55.0,
                      percent=0.8, item=item12, user_id=1)
session.add(renDiv2)
session.commit()

# -----------------------------------------------------------------------

# Carteira de Fundos Imobiliarios
category2 = Category(name="Fundos Imobiliários",
                     description=("Os fundos imobiliários "
                                  "são fundos de"
                                  " investimentos geridos "
                                  "e administrados por"
                                  " um gestor/adminsitrador,"
                                  " que tem como objetivo "
                                  "investiver em ativos "
                                  "imobiliários de"
                                  " determinadas classes "
                                  "e perfis como lajes corporativas,"
                                  " shoppings,"
                                  " galpões logísticos, "
                                  "empreendimentos residenciais,"
                                  " hospitais,"
                                  " e etc, mas também que"
                                  "pode investir em ativos"
                                  " de dívida imobiliária,"
                                  " como LCI, CRI e etc. "
                                  "Possuem uma menor "
                                  "volatilidade quando comparados"
                                  " a ações e uma boa rentabilidade."),
                     user_id=1)
session.add(category2)
session.commit()
# Assets
# 1
item1 = Item(name="Malls Brasil Plural",
             active="MALL11",
             dy="7.1%",
             price="R$106,97",
             description="Tipo: Tijolo-Shoppings",
             category=category2, user_id=1)
session.add(item1)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item1, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='Feb', money=55.0,
                      percent=0.8, item=item1, user_id=1)
session.add(renDiv2)
session.commit()
renDiv3 = Rentability(month='Mar', money=49.0,
                      percent=0.7, item=item1, user_id=1)
session.add(renDiv3)
session.commit()
renDiv3 = Rentability(month='Apr', money=55.0,
                      percent=0.8, item=item1, user_id=1)
session.add(renDiv3)
session.commit()
renDiv4 = Rentability(month='May', money=40.0,
                      percent=0.6, item=item1, user_id=1)
session.add(renDiv4)
session.commit()

# 2
item2 = Item(name="Industrial do Brasil",
             active="FIIB11",
             dy="7.7%",
             price="R$436,74",
             description="Tipo: Tijolo-Galpoes",
             category=category2, user_id=1)
session.add(item2)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item2, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='Feb', money=55.0,
                      percent=0.8, item=item2, user_id=1)
session.add(renDiv2)
session.commit()
renDiv3 = Rentability(month='Mar', money=49.0,
                      percent=0.7, item=item2, user_id=1)
session.add(renDiv3)
session.commit()
renDiv3 = Rentability(month='Apr', money=55.0,
                      percent=0.8, item=item2, user_id=1)
session.add(renDiv3)
session.commit()
renDiv4 = Rentability(month='May', money=40.0,
                      percent=0.6, item=item2, user_id=1)
session.add(renDiv4)
session.commit()

# 3
item3 = Item(name="GGR Covepi Renda",
             active="GGRC11",
             dy="9.2%",
             price="R$129,80",
             description="Tipo: Tijolo-Shoppings",
             category=category2, user_id=1)
session.add(item3)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item3,
                      user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='Feb', money=55.0,
                      percent=0.8, item=item3,
                      user_id=1)
session.add(renDiv2)
session.commit()
renDiv3 = Rentability(month='Mar', money=49.0,
                      percent=0.7, item=item3,
                      user_id=1)
session.add(renDiv3)
session.commit()
renDiv3 = Rentability(month='Apr', money=55.0,
                      percent=0.8, item=item3, user_id=1)
session.add(renDiv3)
session.commit()
renDiv4 = Rentability(month='May', money=40.0,
                      percent=0.6, item=item3,
                      user_id=1)
session.add(renDiv4)
session.commit()

# 4
item4 = Item(name="RBR Rendimento High Grade",
             active="RBRR11",
             dy="9.1%",
             price="R$105,25",
             description="Tipo: Papel-CRIs",
             category=category2, user_id=1)
session.add(item4)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item4, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='Feb', money=55.0,
                      percent=0.8, item=item4, user_id=1)
session.add(renDiv2)
session.commit()
renDiv3 = Rentability(month='Mar', money=49.0,
                      percent=0.7, item=item4, user_id=1)
session.add(renDiv3)
session.commit()
renDiv3 = Rentability(month='Apr', money=55.0,
                      percent=0.8, item=item4, user_id=1)
session.add(renDiv3)
session.commit()
renDiv4 = Rentability(month='May', money=40.0,
                      percent=0.6, item=item4, user_id=1)
session.add(renDiv4)
session.commit()

# 5
item5 = Item(name="XP Malls",
             active="XPML11",
             dy="7.2%",
             price="R$106,00",
             description="Tipo: Tijolo-Shoppings",
             category=category2, user_id=1)
session.add(item5)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item5, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='Feb', money=55.0,
                      percent=0.8, item=item5, user_id=1)
session.add(renDiv2)
session.commit()
renDiv3 = Rentability(month='Mar', money=49.0,
                      percent=0.7, item=item5, user_id=1)
session.add(renDiv3)
session.commit()
renDiv3 = Rentability(month='Apr', money=55.0,
                      percent=0.8, item=item5, user_id=1)
session.add(renDiv3)
session.commit()
renDiv4 = Rentability(month='May', money=40.0,
                      percent=0.6, item=item5, user_id=1)
session.add(renDiv4)
session.commit()

# 6
item6 = Item(name="Kinea Índice de Preços",
             active="KNIP11",
             dy="9.4%",
             price="R$111,15",
             description="Tipo: Papel-CRIs",
             category=category2, user_id=1)
session.add(item6)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item6, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='Feb', money=55.0,
                      percent=0.8, item=item6, user_id=1)
session.add(renDiv2)
session.commit()
renDiv3 = Rentability(month='Mar', money=49.0,
                      percent=0.7, item=item6, user_id=1)
session.add(renDiv3)
session.commit()
renDiv3 = Rentability(month='Apr', money=55.0,
                      percent=0.8, item=item6, user_id=1)
session.add(renDiv3)
session.commit()
renDiv4 = Rentability(month='May', money=40.0,
                      percent=0.6, item=item6, user_id=1)
session.add(renDiv4)
session.commit()

# 7
item7 = Item(name="Vinci Shopping Centers",
             active="VISC11",
             dy="7.2%",
             price="R$108,99",
             description="Tipo: Tijolo-Shoppings",
             category=category2, user_id=1)
session.add(item7)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item7, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='Feb', money=55.0,
                      percent=0.8, item=item7, user_id=1)
session.add(renDiv2)
session.commit()
renDiv3 = Rentability(month='Mar', money=49.0,
                      percent=0.7, item=item7, user_id=1)
session.add(renDiv3)
session.commit()
renDiv3 = Rentability(month='Apr', money=55.0,
                      percent=0.8, item=item7, user_id=1)
session.add(renDiv3)
session.commit()
renDiv4 = Rentability(month='May', money=40.0,
                      percent=0.6, item=item7, user_id=1)
session.add(renDiv4)
session.commit()

# 8
item8 = Item(name="Maxi Renda",
             active="MXRF11",
             dy="8.5%",
             price="R$11,03",
             description="Tipo: Papel-CRIs",
             category=category2, user_id=1)
session.add(item8)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item8, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='Feb', money=55.0,
                      percent=0.8, item=item8, user_id=1)
session.add(renDiv2)
session.commit()
renDiv3 = Rentability(month='Mar', money=49.0,
                      percent=0.7, item=item8, user_id=1)
session.add(renDiv3)
session.commit()
renDiv3 = Rentability(month='Apr', money=55.0,
                      percent=0.8, item=item8, user_id=1)
session.add(renDiv3)
session.commit()
renDiv4 = Rentability(month='May', money=40.0,
                      percent=0.6, item=item8, user_id=1)
session.add(renDiv4)
session.commit()

# 9
item9 = Item(name="CSHG Logística",
             active="HGLG11",
             dy="6.2%",
             price="R$159,00",
             description="Tipo: Tijolo-Galpões",
             category=category2, user_id=1)
session.add(item9)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item9, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='Feb', money=55.0,
                      percent=0.8, item=item9, user_id=1)
session.add(renDiv2)
session.commit()
renDiv3 = Rentability(month='Mar', money=49.0,
                      percent=0.7, item=item9, user_id=1)
session.add(renDiv3)
session.commit()
renDiv3 = Rentability(month='Apr', money=55.0,
                      percent=0.8, item=item9, user_id=1)
session.add(renDiv3)
session.commit()
renDiv4 = Rentability(month='May', money=40.0,
                      percent=0.6, item=item9, user_id=1)
session.add(renDiv4)
session.commit()

# 10
item10 = Item(name="Fator Verita",
              active="VRTA11",
              dy="8.9%",
              price="R$137,95",
              description="Tipo: Papel-CRIs",
              category=category2, user_id=1)
session.add(item10)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item10, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='Feb', money=55.0,
                      percent=0.8, item=item10, user_id=1)
session.add(renDiv2)
session.commit()
renDiv3 = Rentability(month='Mar', money=49.0,
                      percent=0.7, item=item10, user_id=1)
session.add(renDiv3)
session.commit()
renDiv3 = Rentability(month='Apr', money=55.0,
                      percent=0.8, item=item10, user_id=1)
session.add(renDiv3)
session.commit()
renDiv4 = Rentability(month='May', money=40.0,
                      percent=0.6, item=item10, user_id=1)
session.add(renDiv4)
session.commit()

# 11
item11 = Item(name="Continental Square Faria Lima",
              active="FLMA11",
              dy="5.0%",
              price="R$3,00",
              description="Tipo: Tijolo-Escritórios",
              category=category2, user_id=1)
session.add(item11)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item11, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='Feb', money=55.0,
                      percent=0.8, item=item11, user_id=1)
session.add(renDiv2)
session.commit()
renDiv3 = Rentability(month='Mar', money=49.0,
                      percent=0.7, item=item11, user_id=1)
session.add(renDiv3)
session.commit()
renDiv3 = Rentability(month='Apr', money=55.0,
                      percent=0.8, item=item11, user_id=1)
session.add(renDiv3)
session.commit()
renDiv4 = Rentability(month='May', money=40.0,
                      percent=0.6, item=item11, user_id=1)
session.add(renDiv4)
session.commit()

# 12
item12 = Item(name="Rio Negro", active="RNGO11", dy="7.0%", price="R$84,89",
              description="Tipo: Tijolo-Escritórios",
              category=category2, user_id=1)
session.add(item12)
session.commit()

renDiv1 = Rentability(month='Jan', money=50.0,
                      percent=0.7, item=item12, user_id=1)
session.add(renDiv1)
session.commit()
renDiv2 = Rentability(month='Feb', money=55.0,
                      percent=0.8, item=item12, user_id=1)
session.add(renDiv2)
session.commit()
renDiv3 = Rentability(month='Mar', money=49.0,
                      percent=0.7, item=item12, user_id=1)
session.add(renDiv3)
session.commit()
renDiv3 = Rentability(month='Apr', money=55.0,
                      percent=0.8, item=item12, user_id=1)
session.add(renDiv3)
session.commit()
renDiv4 = Rentability(month='May', money=40.0,
                      percent=0.6, item=item12, user_id=1)
session.add(renDiv4)
session.commit()

print("added menu items!")
