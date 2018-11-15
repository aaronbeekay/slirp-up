
import shopify
import logging as log
import random

from flask import Flask, render_template, request, abort
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def shopifySetup():
	shop_url = "https://%s:%s@glitchlab.myshopify.com/admin" % ('test', 'testing') 
	shopify.ShopifyResource.set_site(shop_url)

def productListFromInputFormJson( input ):
	
	import pprint; pprint.pprint(input)
	return('1')
	variants = []
	
	# Metadata that applies to all of the objects
	mfg = input['Manufacturer']['Value']
	mpn = input['MPN']['Value']
	title = '{} {}'.format(mfg, mpn)
	handle = stringEnsafen(title)
	common = {	
		'Handle': handle,
		'Title': title,
		'Manufacturer': mfg,
		'MPN': mpn,
		'dimX': input['X-width (in)')]['Value']
		'dimY': input['Y-length (in)']['Value'],
		'dimZ': input['Z-height (in)']['Value']
	}
	
	
	# Create a variant for each condition with inventory
	condQty = {	
		'new': input.get('Qty. new',0),
		'used-likenew': input.get('Qty. used like new',0),
		'used-good': input.get('Qty. used - good',0),
		'used-fair': input.get('Qty. used - fair',0),
		'used-asis': input.get('Qty. used as-is/for parts', 0)		}

	#import pdb; pdb.set_trace() 
		
	#if condQty['new'] > 0:
	if True:
		v = common.copy()
		variantdata = {
			'Option1 Name': 'Condition',
			'Option1 Value': 'New',
			'Barcode': newBarcode(),
			'condition-notes': input['condition-notes']['Value'],
			'Ownership': input['Owner']['Value'],
			'Sunk-cost': input['Purchase price']['Value'],
			'Reserve-price': None,
			'Asking-price': None	}
		v.update(variantdata)
		variants.append(v)
		
	#if condQty['used-likenew'] > 0:
	if True:
		v = common.copy()
		variantdata = {
			'Option1 Name': 'Condition',
			'Option1 Value': 'Used - Like new',
			'Barcode': newBarcode(),
			'condition-notes': input['condition-notes']['Value'],
			'Ownership': input['Owner']['Value'],
			'Sunk-cost': input['Purchase price']['Value'],
			'Reserve-price': None,
			'Asking-price': None	}
		
		v.update(variantdata)
		variants.append(v)
		
	#if condQty['used-good'] > 0:
	if True:
		v = common.copy()
		variantdata = {
			'Option1 Name': 'Condition',
			'Option1 Value': 'Used - Good',
			'Barcode': newBarcode(),
			'condition-notes': input['condition-notes']['Value'],
			'Ownership': input['Owner']['Value'],
			'Sunk-cost': input['Purchase price']['Value'],
			'Reserve-price': None,
			'Asking-price': None	}
		
		v.update(variantdata)
		variants.append(v)
		
	#if condQty['used-fair'] > 0:
	if True:
		v = common.copy()
		variantdata = {
			'Option1 Name': 'Condition',
			'Option1 Value': 'Used - Fair',
			'Barcode': newBarcode(),
			'condition-notes': input['condition-notes']['Value'],
			'Ownership': input['Owner']['Value'],
			'Sunk-cost': input['Purchase price']['Value'],
			'Reserve-price': None,
			'Asking-price': None	}
		
		v.update(variantdata)
		variants.append(v)
		
	#if condQty['used-asis'] > 0:
	if True:
		v = common.copy()
		variantdata = {
			'Option1 Name': 'Condition',
			'Option1 Value': 'Used - as-is/for parts',
			'Barcode': newBarcode(),
			'condition-notes': input['condition-notes']['Value'],
			'Ownership': input['Owner']['Value'],
			'Sunk-cost': input['Purchase price']['Value'],
			'Reserve-price': None,
			'Asking-price': None	}
		
		v.update(variantdata)
		variants.append(v)
		
	# Add the variant information to the product in question
	common['variants'] =  variants
	products.append(common)
	
	return(products)
		
def newBarcode():
	# 5 digit random number
	return ''.join([str(random.randint(0,9)) for i in range(1,6)])
		
def createNewShopifyProductsAndVariants( products ):
	for product in products:
		if len(shopify.Product.find(handle=product['Handle'])) > 0:
			log.warning('tried to add product with handle {} but that product already exists'.format(product['Handle']))
			continue		# Skip to next product
		
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
			va = { 	'option1': v['Option1 Value'],
					'inventory_management': 'shopify',
					'inventory_policy': 'continue',
					'weight': product['Weight(g)'],
					'weight_unit': 'g',
					'metafields': [	fmt('condition-notes', 	v['condition-notes']),
									fmt('Ownership',		v['Ownership']		),
									fmt('Sunk-cost',		v['Sunk-cost']		)		]
					}
			variants.append(va)
		pr.variants = variants
			
		pr.options = [	{	"name": "Condition",
							"position": 1,
							"values": ["New", "Used - Like new", "Used - Good", "Used - Fair", "Used - as-is/for parts"]}		]
		
	
		
		if pr.save() is False:
			message = 'Couldn\'t save product {}. Error messages: {}...'.format(
					pr.handle, 
					pr.errors.full_messages()	)
			log.error(message)
			raise RuntimeError(message)
		else:
			log.info('Successfully created product id {} - {}'.format(pr.id, pr.handle))
			
""" Endpoints """
@app.route('/api/intake', methods=['POST'])
def make_products():
	log.debug('Got a POST request here at the intake.')
	if not request.json or not request.json['answers']:
		log.warning('Request body is not suitable: \n{}'.format(request.data))
		abort(400)
	
	log.debug('We got a live one. Here it is.')
	products = productListFromInputFormJson(request.json['answers'])
	socketio.emit('newproduct', {'data': products})
	return(str(products))
	
@socketio.on('connect')
def connect_notification():
	log.debug('someone is here')
	socketio.emit('notice', 'somebody is here')
	
@socketio.on('disconnect')
def disconnnect_notification():
	log.debug('someone is here')
	socketio.emit('notice', 'somebody left')

if __name__ == "__main__":
	log.basicConfig(level=log.DEBUG, format='%(asctime)s %(message)s')
	socketio.run(app)
	
