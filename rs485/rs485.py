import minimalmodbus #rs485
import logging

log = logging.getLogger(__name__)




class rsReader(object):
	defaults = {
	'device': '/dev/ttyUSB0',
	'devicenumber': 1,
	'baudrate': 9600,
	'bytesize': 8,
	'stopbits': 1,
	'timeout': 5,
	}

	def __init__(self, **kwargs):
		config = {}
       		config.update(self.defaults)
        	config.update(kwargs)

		#init rs485 
		self.rs485 = minimalmodbus.Instrument( config['device'], config['devicenumber'])
		self.rs485.mode =  minimalmodbus.MODE_RTU
		self.rs485.serial.parity =  minimalmodbus.serial.PARITY_NONE
		#rs485.debug = Config.get('rs485', 'debug')
		self.rs485.serial.baudrate = int(config['baudrate'])
		self.rs485.serial.bytesize = int(config['bytesize'])
		self.rs485.serial.stopbits = int(config['stopbits'])
		self.rs485.serial.timeout = int(config['timeout'])


	def readRS485(self, eqid ):
		if not eqid:
			log.info('Geen Equipment ID beschikbaar!')
			raise EqidError('No Eqid found! ')
		else:	
			''' read DSM120 powermeter over rs485 '''
			ret = {}
			try:
				Activepower =  self.rs485.read_float( 12, functioncode=4, numberOfRegisters=2)
				TotalPower =  self.rs485.read_float( 342, functioncode=4, numberOfRegisters=2)
			except IOError as err:
				log.info( 'Ooops, rs458 hickups %s' % err)
				pass
			else:
				ret['sol_pow'] = abs(float(Activepower))
				ret['sol_nrg'] = abs(float(TotalPower))

			return ret

class EqidError(Exception):
	pass