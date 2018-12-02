
import shopify
import logging
import random

from flask import Flask, render_template, request, abort
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# create logger with 'spam_application'
logger = logging.getLogger('straw.slirp.aaronbeekay')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('straw.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

if __name__ != '__main__':	# only do this when running w gunicorn
	glogs = logging.getLogger('gunicorn.error')
	# don't need to put time in logs because it's already there
	formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
	
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	for h in glogs.handlers:
		h.setFormatter(formatter)
		#logger.setLevel(logging.DEBUG, h)
		logger.addHandler(h)
		
		
		
		
try:
	SHOPIFY_API_KEY = os.environ['SHOPIFY_API_KEY']
	SHOPIFY_API_PASSWORD = os.environ['SHOPIFY_API_PASSWORD']
except KeyError:
	raise ValueError('Didn\'t find API key or password in env vars')
	
shop_url = "https://%s:%s@glitchlab.myshopify.com/admin" % (SHOPIFY_API_KEY, SHOPIFY_API_PASSWORD)
shopify.ShopifyResource.set_site(shop_url)

def stringEnsafen(s):
	try:
		#import pdb; pdb.set_trace()
		s = s.strip().replace('	 ', ' ').replace(' ', '-')
		return ''.join(filter(lambda c: c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~-_.', s))
	except:
		return ""
	pass

def safeGet(dict,key1,key2):
	r = None
	if dict.get(key1) is not None:
		r = dict.get(key1)
		if key2 is not None and key2 in r:
			r = r.get(key2)

	if r is None:
		r = 0
	
	return(r)
	

def productListFromInputFormJson( input ):
	variants = []
	products = []
	
	# Metadata that applies to all of the objects
	mfg = safeGet(input, 'Manufacturer', 'value')
	mpn = safeGet(input, 'MPN', 'value')
	title = '{} {}'.format(mfg, mpn)
	handle = stringEnsafen(title)
	common = {
		'Handle': handle,
		'Title': title,
		'Manufacturer': mfg,
		'MPN': mpn,
		'Weight(g)': float(safeGet(input,'Weight__g_','value')),
		'dimX': float(safeGet(input, 'X_width__in_', 'value')),
		'dimY': float(safeGet(input, 'Y_length__in_', 'value')),
		'dimZ': float(safeGet(input, 'Z_height__in_', 'value'))
	}

	logger.debug('Just gonna go ahead and put together a product listing for {}'.format(handle))


	# Create a variant for each condition with inventory
	condQty = {
	'new': int(safeGet(input, 'Qty__new', 'value')),
	'used-likenew': int(safeGet(input, 'Qty__used_like_new', 'value')),
	'used-good': int(safeGet(input, 'Qty__used___good', 'value')),
	'used-fair': int(safeGet(input, 'Qty__used___fair', 'value')),
	'used-asis': int(safeGet(input, 'Qty__used_as_is_for_parts', 'value'))		}

	common['x-condQty'] = condQty.values()

	#import pdb; pdb.set_trace()

	#if condQty['new'] > 0:
	if True:
		v = common.copy()
		variantdata = {
			'Option1 Name': 'Condition',
			'Option1 Value': 'New',
			'barcode': newBarcode(),
			'condition-notes': safeGet(input, 'condition-notes', 'value'),
			'Ownership': safeGet(input, 'Owner', 'value'),
			'Sunk-cost': float(safeGet(input, 'Purchase_price', 'value')),
			'Reserve-price': None,
			'Asking-price': None,
			'qty-reported': condQty['new']
			}
		v.update(variantdata)
		variants.append(v)

	#if condQty['used-likenew'] > 0:
	if True:
		v = common.copy()
		variantdata = {
			'Option1 Name': 'Condition',
			'Option1 Value': 'Used - Like new',
			'barcode': newBarcode(),
			'condition-notes': safeGet(input, 'condition-notes', 'value'),
			'Ownership': safeGet(input, 'Owner', 'value'),
			'Sunk-cost': float(safeGet(input, 'Purchase_price', 'value')),
			'Reserve-price': None,
			'Asking-price': None,
			'qty-reported': condQty['used-likenew']	
		}

		v.update(variantdata)
		variants.append(v)

	#if condQty['used-good'] > 0:
	if True:
		v = common.copy()
		variantdata = {
			'Option1 Name': 'Condition',
			'Option1 Value': 'Used - Good',
			'barcode': newBarcode(),
			'condition-notes': safeGet(input, 'condition-notes', 'value'),
			'Ownership': safeGet(input, 'Owner', 'value'),
			'Sunk-cost': float(safeGet(input, 'Purchase_price', 'value')),
			'Reserve-price': None,
			'Asking-price': None,
			'qty-reported': condQty['used-good']	}

		v.update(variantdata)
		variants.append(v)

	#if condQty['used-fair'] > 0:
	if True:
		v = common.copy()
		variantdata = {
			'Option1 Name': 'Condition',
			'Option1 Value': 'Used - Fair',
			'barcode': newBarcode(),
			'condition-notes': safeGet(input, 'condition-notes', 'value'),
			'Ownership': safeGet(input, 'Owner', 'value'),
			'Sunk-cost': float(safeGet(input, 'Purchase_price', 'value')),
			'Reserve-price': None,
			'Asking-price': None,
			'qty-reported': condQty['used-fair']	}

		v.update(variantdata)
		variants.append(v)

	#if condQty['used-asis'] > 0:
	if True:
		v = common.copy()
		variantdata = {
			'Option1 Name': 'Condition',
			'Option1 Value': 'Used - as-is/for parts',
			'barcode': newBarcode(),
			'condition-notes': safeGet(input, 'condition-notes', 'value'),
			'Ownership': safeGet(input, 'Owner', 'value'),
			'Sunk-cost': float(safeGet(input, 'Purchase_price', 'value')),
			'Reserve-price': None,
			'Asking-price': None,
			'qty-reported': condQty['used-asis']	}

		v.update(variantdata)
		variants.append(v)

	# Add the variant information to the product in question
	common['variants'] =  variants
	products.append(common)

	logger.debug('Product listing looks good.')

	return(products)

def newBarcode():
	# 5 digit random number
	return ''.join([str(random.randint(0,9)) for i in range(1,6)])

def createNewShopifyProductAndVariants( product ):
	#shopify.ShopifyResource.activate_session(session)
	
	logger.debug('I think the product handle is {}'.format(product['Handle']))
	import pprint
	logger.debug( pprint.pformat(product))
	if len(shopify.Product.find(handle=product['Handle'])) > 0:
		logger.warning('tried to add product with handle {} but that product already exists'.format(product['Handle']))
		abort(400)

	pr = shopify.Product()
	pr.title = product['Title']

	fmt = lambda key,value: {	"key": key,
								"value": value,
								"value_type": "string",		# TODO do this right
								"namespace": "Namespace"}

	pr.metafields = [	fmt('Manufacturer', product['Manufacturer']),
						fmt('MPN', product['MPN']),
						fmt('dimX', product['dimX']),
						fmt('dimY', product['dimY']),
						fmt('dimZ', product['dimZ'])		]

	variants = []
	for v in product['variants']:
		va = {	'option1': v['Option1 Value'],
				'inventory_management': 'shopify',
				'inventory_policy': 'continue',
				'weight': product['Weight(g)'],
				'weight_unit': 'g',
				'metafields': [ fmt('condition-notes',	v['condition-notes']),
								fmt('Ownership',		v['Ownership']		),
								fmt('Sunk-cost',		v['Sunk-cost']		)		]
				}
		variants.append(va)
	pr.variants = variants

	pr.options = [	{	"name": "Condition",
						"position": 1,
						"values": ["New", "Used - Like new", "Used - Good", "Used - Fair", "Used - as-is/for parts"]}		]


	logger.debug('Trying to save product to Shopify...')

	if pr.save() is False:
		message = 'Couldn\'t save product {}. Error messages: {}...'.format(
				product['Handle'],
				pr.errors.full_messages()	)
		logger.error(message)
		raise RuntimeError(message)
	else:
		logger.info('Successfully created product id {} - {}'.format(pr.id, pr.handle))
		logger.debug('Trying to set barcodes for variants...')
		for i,var in enumerate(product['variants']):
			v = pr.variants[i]
			if v.option1 == var['Option1 Value']:	# this is the right new/used variant (avoid counting errors)
				v.barcode = var['barcode']
			logger.debug('Assigned barcode {} to variant {}...'.format(v.barcode, v.option1))
		
		pr.save() # TODO second round of error checking on this one
		
		qtystr = ','.join( [ str(product['variants'][i]['Option1 Value']) + "," + str(product['variants'][i]['qty-reported']) for i in range(len(product['variants']))])
		logger.info('Reported quantities: {}'.format(qtystr))
		return((id,product))

""" Endpoints """
@app.route('/api/intake', methods=['POST'])
def make_products():
	logger.debug('Got a POST request here at the intake.')
	logger.debug('The raw request is {}'.format(request.data))
	if not request.json or not request.json['answers']:
		logger.warning('Request body is not suitable: \n{}'.format(request.data))
		abort(400)

	with open('last-request.json', 'w') as outfile:
		import json
		json.dump(request.json, outfile)

	logger.debug('We got a live one. Here it is.')
	products = productListFromInputFormJson(request.json['answers'])

	#import pprint; logger.debug(pprint.pformat(products))

	id,prod = createNewShopifyProductAndVariants(products[0])
	qtys = [ prod['variants'][i]['qty-reported'] for i in range(len(prod['variants']))]
	logger.debug(qtys)
	barcodes = [ prod['variants'][i]['barcode'] for i in range(len(prod['variants']))]
	logger.debug(barcodes)
	name = prod['Title']
	
	socketio.emit('newproduct',[name,qtys,barcodes])
	
	#socketio.emit('newproduct', json.dumps(newpr.__dict__))

	return(str(products))

@socketio.on('connect')
def connect_notification():
	logger.debug('someone is here')
	socketio.emit('notice', 'somebody is here')

@socketio.on('disconnect')
def disconnnect_notification():
	logger.debug('someone is here')
	socketio.emit('notice', 'somebody left')
	
@socketio.on('lookup'):
def lookup_barcode(bc):
	try:
		sku = int(bc)		# see if it is a valid numbah
	except ValueError:
		logger.info('Invalid barcode lookup request: got {}'.format(bc))
		
	v = shopify.
	


if __name__ == "__main__":
	socketio.run(app)
