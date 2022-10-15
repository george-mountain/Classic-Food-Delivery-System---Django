import datetime




def generate_order_number(pk):
    current_date_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    order_number = current_date_time + str(pk)

    return order_number