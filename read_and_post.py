from smeterd.meter import SmartMeter
from influx.influxpost import post
import logging 
logging.info('Starting up!')



# create logger with 'spam_application'
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)


log.addHandler(ch)
log.info('creating an instance of log')

meter = SmartMeter('/dev/ttyAMA0', baudrate=115200)

while True:
	packet = meter.read_one_packet()
	eqid = str(packet['kwh']['eid']).decode('hex')
	tariff = packet['kwh']['tariff']

	body=''
	bodyTemplate_energy = 'emeter_energy,eqid='+ eqid +',tarif={tarif},direction={dir} value={value}\n'
	bodyTemplate_power = 'emeter_power,eqid='+ eqid +',tarif={tarif},direction={dir},phase={phase} value={value}\n'

	body += bodyTemplate_energy.format( dir='in', tarif='1', value=packet['kwh']['high']['consumed'] )
	body += bodyTemplate_energy.format( dir='out', tarif='1', value=packet['kwh']['high']['produced'] )
	body += bodyTemplate_energy.format( dir='in', tarif='2', value=packet['kwh']['low']['consumed'] )
	body += bodyTemplate_energy.format( dir='out', tarif='2', value=packet['kwh']['low']['produced'] )

	body += bodyTemplate_power.format( dir='in', tarif=tariff, phase='L1', value=packet['kwh']['current_consumed_phaseOne'] )
	body += bodyTemplate_power.format( dir='in', tarif=tariff, phase='L2', value=packet['kwh']['current_consumed_phaseTwo'] )
	body += bodyTemplate_power.format( dir='in', tarif=tariff, phase='L3', value=packet['kwh']['current_consumed_phaseThree'] )
	body += bodyTemplate_power.format( dir='in', tarif=tariff, phase='total', value=packet['kwh']['current_consumed'] )

	body += bodyTemplate_power.format( dir='out', tarif=tariff, phase='L1', value=packet['kwh']['current_produced_phaseOne'] )
	body += bodyTemplate_power.format( dir='out', tarif=tariff, phase='L2', value=packet['kwh']['current_produced_phaseTwo'] )
	body += bodyTemplate_power.format( dir='out', tarif=tariff, phase='L3', value=packet['kwh']['current_produced_phaseThree'] )
	body += bodyTemplate_power.format( dir='out', tarif=tariff, phase='total', value=packet['kwh']['current_produced'] )

	poster = post()
	poster.httpsPost(body)