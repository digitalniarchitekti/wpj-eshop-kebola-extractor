import json
import warnings
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import datetime
from keboola.component import CommonInterface
import csv


ci = CommonInterface()
params = ci.configuration.parameters


transport = AIOHTTPTransport(url= params["url"], headers={'X-Access-Token': params['#token']})
client = Client(transport=transport, fetch_schema_from_transport=True)




def get_oder(id):

    query = gql(
        """{{
            order(id: {}) {{
    id
    code
    dateCreated
    status
    deliveryAddress {{
      name
      surname
      street
      city
      zip
      country {{
        code
        name
      }}
    }}
    items {{
      name
      pieces
      totalPrice {{
        withVat
        vat
        currency {{
          code
        }}
      }}
    }}
  }}
}}""".format(id)
    )
    result = client.execute(query)
    return result['order']


def get_products(id):
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
    This function load oders from x last x days
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
        orders(limit: 10000000, sort: {{ dateCreated: DESC }}, filter: {{ dateFrom:"{}"}}) {{
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
    orders = get_orders(num_of_days=params["num_of_days"])

    order_lst = []
    for i in orders:
        order_lst.append(get_oder(i['id']))

    json_product = json.dumps(order_lst)
    json_oders = json.dumps(orders)


    output = {
        "orders": orders,
        "order": order_lst
    }
    x = json.dumps(output)

    result_table = ci.create_out_table_definition('orderes_detail.csv', primary_key=['id'],incremental=True)

    with open(result_table.full_path, 'w', newline='',encoding='utf-8') as csv_oders:
        writer = csv.writer(csv_oders)
        writer.writerow(("id", "code","dateCreated","status","deliveryAddress","items"))
        for i in order_lst:
            writer.writerow((i["id"], i["code"],i['dateCreated'],i["status"],str(i['deliveryAddress']),str(i["items"])))
        csv_oders.close()
    result_table.table_metadata.add_table_description("Orders for given time period")
    result_table.table_metadata.add_column_data_types({"id":"INTEGER","code":"INTEGER","dateCreated":"DATE",
                                                       "status":"INTEGER","deliveryAddress":"STRING","items":"STRING"})
    ci.write_manifest(result_table)
    print("done")