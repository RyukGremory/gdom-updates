import requests
import urllib
import socket

webRequestURI='domains.google.com/nic/update'
username='AutoGenerate in Google Domains Admin console'
password='AutoGenerate in Google Domains Admin console'
sub_domain='@ or lab,'
domain='domain'
tld='com,net,org'


def ResponseHandling(response):
    Gresponses = {
        "good" : "Success: The update was successful. You should not attempt another update until your IP address changes.",
		"nochg" : "Success: The supplied IP address is already set for this host. You should not attempt another update until your IP address changes.", 
		"nohost" : "Error: The hostname does not exist, or does not have Dynamic DNS enabled.",
		"badauth" : "Error: The username / password combination is not valid for the specified host.",
		"notfqdn" : "Error: The supplied hostname is not a valid fully-qualified domain name.",
		"badagent" : "Error: Your Dynamic DNS client is making bad requests. Ensure the user agent is set in the request, and that you’re only attempting to set an IPv4 address. IPv6 is not supported.",
		"abuse" : "Error: Dynamic DNS access for the hostname has been blocked due to failure to interpret previous responses correctly.",
		"911" : "Error: An error happened on our end. Wait 5 minutes and retry.",
        "Nocambio":"There is not update, the IPs are the same"
        }
    response = Gresponses[response.split(' ')[0]]
    return response


def Update_process(username,password,webRequestURI,sub_domain,domain,tld):
    ## Obtenemos la IP publica que tiene el dispositivo donde se esta ejecutando el script
    localIp = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    ## Obtenemos la IP que tiene el dominio actualmente
    domainIp = socket.gethostbyname('{}.{}.{}'.format(sub_domain,domain,tld))
    ## Si las IP son diferentes, se procede a actualizar
    if localIp != domainIp:
        ## se construye la URI para hacer el update. https://support.google.com/domains/answer/6147083?hl=en
        URI = 'https://{}:{}@{}?hostname={}.{}.{}&myip={}'.format(username,password,webRequestURI,sub_domain,domain,tld,localIp)
        ## Se realiza el update (post)
        update = requests.post(URI)
        ## Captura el response, pensare si lo mando a log o no.
        response = ResponseHandling(update.text)
    ## Si la IP no cambio no se hace nada, pensare si lo mando a log o no.
    elif localIp == domainIp:
        response = ResponseHandling('Nocambio')
    ## Cualquier otra situacion no se toma en cuenta, pensare si lo mando a log o no.
    else:
        pass
    return response


if __name__ == "__main__":
    try:
        Update_process(username,password,webRequestURI,sub_domain,domain,tld)
    except:
        pass
