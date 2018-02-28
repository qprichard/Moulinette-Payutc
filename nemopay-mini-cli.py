import csv 
import sys, getopt, os.path
import requests
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

headers = {
		'Content-Type': 'application/json',
		'Nemopay-Version': '2017-12-15',
}

def readCsv(inputfile,action,sessionid,fundation):
	with open(inputfile, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		if action=="addGroup":
			lastparam=getWalletGroups(sessionid)
			callable=addWalletToGroup
		elif action=="addRight":
			lastparam=fundation
			callable=addRightToWallet
		for row in spamreader:
			if(row[0]+row[1]+row[2]!=''):
				callable(getWalletId(row[0]+' '+row[1]+' '+row[2],sessionid),row[3],sessionid,lastparam)
				
def getWalletGroups(sessionid):
	print bcolors.HEADER + 'Getting wallet groups' + bcolors.ENDC
	params = (
		('event', '1'),
		('ordering', 'id'),
		('system_id', 'payutc'),
		('active', True),
		('sessionid', sessionid),
	)
	response = requests.get('https://api.nemopay.net/resources/walletgroups', headers=headers, params=params)
	if response.status_code==200:
		ret = {}
		for group in response.json():
			ret[group['id']]=group['name']
		return ret
	else:
		print bcolors.FAIL + "FAIL (unhandled error)" + bcolors.ENDC
		print response.json()
		sys.exit(9)
		
def getWalletId(user,sessionid):

	print bcolors.OKBLUE + 'Getting ' + user + ' wallet id ' + bcolors.ENDC
	params = (
		('system_id', 'payutc'),
		('sessionid', sessionid),
	)
	data = '{"queryString":"'+str(user)+'","wallet_config":1}'

	response = requests.post('https://api.nemopay.net/services/GESUSERS/walletAutocomplete', headers=headers, params=params, data=data)
	if response.status_code == 403:
		print bcolors.FAIL + "FAIL (Forbidden, maybe a bad session id is used)" + bcolors.ENDC
		print bcolors.FAIL + "Exiting" + bcolors.ENDC
		sys.exit(6)
	elif response.json() == []:
		print bcolors.FAIL + "FAIL (account not found)" + bcolors.ENDC
		print bcolors.FAIL + "Exiting" + bcolors.ENDC
		sys.exit(7)
	elif response.status_code==200:
		return str(response.json()[0]['id'])
	else:
		print bcolors.FAIL + "FAIL (unhandled error)" + bcolors.ENDC
		print response.json()
		sys.exit(8)
			
def addWalletToGroup(wallet,walletGroup,sessionid,walletgroups):

	params = (
		("system_id", 'payutc'),
		("sessionid", sessionid),
	)

	print bcolors.OKBLUE + 'Adding wallet ' + str(wallet) + ' to group ' + walletgroups[int(walletGroup)] + bcolors.ENDC

	data = '{"wallet_id":'+str(wallet)+'}'

	response = requests.post('https://api.nemopay.net/resources/walletgroups/'+walletGroup+'/members', headers=headers, params=params, data=data)

	if response.status_code == 204:
		print bcolors.OKGREEN + "OK" + bcolors.ENDC
	else:
		print bcolors.FAIL + "FAIL (cannot add to group)" + bcolors.ENDC
		
def addRightToWallet(wallet,permission,sessionid,fundation):

	params = (
		("system_id", 'payutc'),
		("sessionid", sessionid),
	)

	print bcolors.OKBLUE + 'Adding permission ' + str(permission) + ' to wallet ' + str(wallet) + ' on fundation ' + str(fundation) + bcolors.ENDC

	data = '{"obj":'+wallet+',"fundation":'+fundation+',"location":null,"event":1,"name":"'+permission+'"}'

	response = requests.post('https://api.nemopay.net/resources/walletrights', headers=headers, params=params, data=data)

	if response.status_code == 201:
		print bcolors.OKGREEN + "OK" + bcolors.ENDC
	else:
		print bcolors.FAIL + "FAIL (cannot add permission)" + bcolors.ENDC
			
def main(argv):
	action = ''
	sessionid = ''
	inputfile = ''
	fundation = 'null'
	helper = sys.argv[0] + ' -i <inputfile> -a <addGroup|addRight> -s <sessionid> [-f <fundationid>]'
	try:
		opts, args = getopt.getopt(argv,"hf:i:a:s:",["help","ifile=","action=","sessionid=","fundation="])
	except getopt.GetoptError as msg:
		print msg
		print helper
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print helper
			sys.exit()
		elif opt in ("-i", "--inputfile"):
			if os.path.isfile(os.path.abspath(arg)):
				inputfile = arg			
			else:
				print bcolors.FAIL + "FAIL ( file " + arg + " does not exist )" + bcolors.ENDC
				sys.exit(3)
		elif opt in ("-a", "--action"):
			if arg == "addGroup" or arg == "addRight":
				action = arg
			else:
				print bcolors.FAIL + "FAIL ( " + arg + " is not a valid action )" + bcolors.ENDC
				sys.exit(4)
		elif opt in ("-s", "--sessionid"):
			sessionid = arg
		elif opt in ("-f", "--fundation"):
			fundation = str(arg)
	if action == '' or sessionid == '' or inputfile == '' or fundation == '':
		print helper
		sys.exit(5)
	readCsv(inputfile,action,sessionid,fundation)
	
			
if __name__ == "__main__":
	main(sys.argv[1:])
