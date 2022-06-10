import json
import warnings
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import datetime

transport = AIOHTTPTransport(url="https://hannah.wpj.cloud/admin/graphql/", headers={'X-Access-Token': token})
client = Client(transport=transport, fetch_schema_from_transport=True)


def get_product(id):
    """
    Return products of given ID
    :param id: Id of products
    :type id: int
    :return: products details
    :rtype: Dict
    """
    # Todo implement more stuff from https://graphql-docs.wpjshop.cz/
    query = gql(
        """{{
        product(id:{}){{
        id
        variationId
        url
        code
        ean
        inStore
        title
        variationTitle
        description
        }}
        }}""".format(id)
    )
    result = client.execute(query)
    return result['product']


def get_orders(num_of_days=7):
    """
    This function load oders from x last x days TODO implement next day
    :param num_of_days: Num of days in history to load
    :type num_of_days: int
    :return: List of history oders
    :rtype: Dict
    """
    date = datetime.datetime.now() - datetime.timedelta(days=num_of_days)
    date = date.isoformat()
    query = gql(
        """
        {{
        orders(limit: 10000, sort: {{ dateCreated: DESC }}, filter: {{ dateFrom:"{}"}}) {{
        hasNextPage
        hasPreviousPage
        items {{
        id
        code
        dateCreated
        totalPrice {{
            withVat
            withoutVat
        }}
        currency {{
            code
            name
        }}
        }}
        }}
    }}
    """.format(date)
    )
    result = client.execute(query)

    if (result["orders"]["hasNextPage"] or result["orders"]["hasPreviousPage"]):
        warnings.warn("Next_page not implemented", Warning)

    return result["orders"]["items"]


if __name__ == '__main__':
    orders = get_orders()

    product_lst = []
    for i in orders:
        product_lst.append(get_product(i['id']))
    print(product_lst)
    print(orders)