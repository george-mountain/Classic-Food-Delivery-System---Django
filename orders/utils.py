import datetime
import simplejson as json



def generate_order_number(pk):
    current_date_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    order_number = current_date_time + str(pk)

    return order_number


def order_total_by_vendor(order, vendor_id):
    total_data = json.loads(order.total_data)
    data = total_data.get(str(vendor_id))
    subtotal = 0
    tax = 0
    tax_dict = {}

    for key,val in data.items():

    
        subtotal += float(key)
        val = val.replace("'",'"')
        val = json.loads(val)
        tax_dict.update(val)

        # calculate the tax per vendor now
        # {'CGST':{'6.00': '4.43'},'SGST':{'5.34':'2.66'}} this is how the tax data looks like
        for i in val:
            
            for j in val[i]:
                tax += float(val[i][j])
    grand_total = float(subtotal) + float(tax)
    context = {
        'subtotal': subtotal,
        'tax_dict': tax_dict,
        'grand_total': grand_total,
    }
    return context