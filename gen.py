const_variables = """\nexport IMAGE_TAG="latest"
export CONFIGTX_ORDERER_BATCHSIZE_MAXMESSAGECOUNT=10
export CONFIGTX_ORDERER_BATCHTIMEOUT=2s
export KAFKA_DEFAULT_REPLICATION_FACTOR=3
export CORE_LOGGING_GOSSIP=WARNING
export ORDERER_GENERAL_TLS_ENABLED=false
export ORDERER_GENERAL_TLS_PRIVATEKEY=/var/hyperledger/tls/server.key
export ORDERER_GENERAL_TLS_CERTIFICATE=/var/hyperledger/tls/server.crt
export ORDERER_TLS_CLIENTAUTHREQUIRED=false
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_TLS_CERT_FILE=/var/hyperledger/tls/server.crt
export CORE_PEER_TLS_KEY_FILE=/var/hyperledger/tls/server.key
export CORE_PEER_TLS_CLIENTAUTHREQUIRED=false
export ORDERER_ABSOLUTEMAXBYTES="10 MB"
export ORDERER_PREFERREDMAXBYTES="512 KB"
export KAFKA_MESSAGE_MAX_BYTES="1000012 B"
export KAFKA_REPLICA_FETCH_MAX_BYTES="1048576 B"
export KAFKA_REPLICA_FETCH_RESPONSE_MAX_BYTES="10485760 B"
export ARCH=$(arch)"""

#Put "number1" space and "number" line jump 
def jumptab(number, number1):
    i = 0
    rslt = ""
    while (i < number):
        rslt = rslt + '\n'
        i += 1
    i = 0
    while (i < number1):
        rslt = rslt + "  "
        i += 1
    return (rslt)

#Part of configtx.yaml
def createOrgPolicies(policy):
    rslt = "Policies:"
    rslt += jumptab(1,2) + "Readers:"
    rslt += jumptab(1,2) + "Rule: "


#Part of configtx.yaml
def createChannelProfile(orgName, profileName):
    rslt = jumptab(0, 1) + profileName + ":"
    rslt += jumptab(1, 2) + "Consortium: ComposerConsortium"
    rslt += jumptab(1, 2) + "Application:"
    rslt += jumptab(1, 3) + "<<: *ApplicationDefaults"
    rslt += jumptab(1, 3) + "Organizations:"
    i = 2
    while (i < len(orgName)):
        rslt += jumptab(1, 5) + "- *" + orgName[i]
        i += 2
    #rslt += jumptab(1, 3) + "Capabilities:"
    #rslt += jumptab(1, 5) + "<<: *ApplicationCapabilities"
    return (rslt)

#Part of configtx.yaml
def createProfiles(orgName, profileName, ordererName):
    rslt = jumptab(0, 1) + profileName + ":"
    #rslt += jumptab(1, 2) + "<<: *ChannelDefaults"
    rslt += jumptab(1, 2) + "Orderer:"
    rslt += jumptab(1, 3) + "<<: *OrdererDefaults"
    rslt += jumptab(1, 3) + "Organizations:"
    rslt += jumptab(1, 4) + "- *" + ordererName
    #rslt += jumptab(1, 3) + "Capabilities:"
    #rslt += jumptab(1, 4) + "<<: *OrdererCapabilities"
    rslt += jumptab(1, 2) + "Consortiums:"
    rslt += jumptab(1, 3) + "ComposerConsortium:"
    rslt += jumptab(1, 4) + "Organizations:"
    i = 2
    while (i < len(orgName)):
        rslt += jumptab(1, 5) + "- *" + orgName[i]
        i += 2
    return (rslt)

#Part of configtx.yaml
def createOrganisations(name, opt, host, policy="OR"):
    rslt = jumptab(0, 1) + "- &" + name
    rslt = rslt + jumptab(2, 3) + "Name: " + name +"MSP" if name is not "OrdererOrg" else rslt + jumptab(2, 3) + "Name: " + name
    if (opt == 1):
        rslt = rslt + jumptab(2, 3) + "ID: " + name + "MSP"
        rslt = rslt + jumptab(2, 3) + "MSPDir: crypto-config/peerOrganizations/" + name + "." + host + ".com/msp"
        #rslt = createPolicyOrg(name, policy, rslt)
    else:
        rslt = rslt + jumptab(2, 3) + "ID: OrdererMSP"
        rslt = rslt + jumptab(2, 3) + "MSPDir: crypto-config/ordererOrganizations/" + host + ".com/msp"
        #rslt = createPolicyOrdererOrg(name, policy, rslt)
    #rslt = rslt + jumptab(2, 3) + "AdminPrincipal: Role.MEMBER"

    if (opt == 1):
        rslt = rslt + jumptab(2, 3) + "AnchorPeers:"
        rslt = rslt + jumptab(2, 4) + "- Host: peer0." + name + "." + host + ".com"
        rslt = rslt + jumptab(1, 4) + "  Port: 7051"
    return (rslt)

def createCapabilities():
    res = "Capabilities:"
    res += jumptab(2,1) + "Channel: &ChannelCapabilities"
    res += jumptab(1,2) + "V1_3: true"
    res += jumptab(2,1) + "Orderer: &OrdererCapabilities"
    res += jumptab(1,2) + "V1_1: true"
    res += jumptab(2, 1) + "Application: &ApplicationCapabilities"
    res += jumptab(1, 2) + "V1_3: true"
    res += jumptab(1, 2) + "V1_2: false"
    res += jumptab(1, 2) + "V1_1: false"
    return res

def createChannelConfigtx():
    res = "Channel: &ChannelDefaults"
    res += jumptab(1,1) + createOtherPolicy("")
    res += jumptab(1,1) + "Capabilities:"
    res += jumptab(1,2) + "<<: *ChannelCapabilities"
    return res

def createPolicyOrdererOrg(name, policy, rslt):
    rslt = rslt + jumptab(2, 3) + "Policies:"
    rslt = rslt + jumptab(1, 5) + "Readers:"
    rslt = rslt + jumptab(1, 7) + "Type: Signature"
    rslt = rslt + jumptab(1, 7) + "Rule: " + policy + "('{0}')".format(name + "MSP.member")
    rslt = rslt + jumptab(1, 5) + "Writers:"
    rslt = rslt + jumptab(1, 7) + "Type: Signature"
    rslt = rslt + jumptab(1, 7) + "Rule: " + policy + "('{0}')".format(name + "MSP.member")
    rslt = rslt + jumptab(1, 5) + "Admins:"
    rslt = rslt + jumptab(1, 7) + "Type: Signature"
    rslt = rslt + jumptab(1, 7) + "Rule: " + policy + "('{0}')".format(name + "MSP.admin")
    return rslt

def createPolicyOrg(name, policy, rslt):
    rslt = rslt + jumptab(2, 3) + "Policies:"
    rslt = rslt + jumptab(1, 5) + "Readers:"
    rslt = rslt + jumptab(1, 7) + "Type: Signature"
    rslt = rslt + jumptab(1, 7) + "Rule: \"" + policy + "('{0}','{1}','{2}')\"".format(name + "MSP.admin",
                                                                                   name + "MSP.peer",
                                                                                   name + "MSP.client")
    rslt = rslt + jumptab(1, 5) + "Writers:"
    rslt = rslt + jumptab(1, 7) + "Type: Signature"
    rslt = rslt + jumptab(1, 7) + "Rule: \"" + policy + "('{0}','{1}')\"".format(name + "MSP.admin", name + "MSP.client")
    rslt = rslt + jumptab(1, 5) + "Admins:"
    rslt = rslt + jumptab(1, 7) + "Type: Signature"
    rslt = rslt + jumptab(1, 7) + "Rule: \"" + policy + "('{0}')\"".format(name + "MSP.admin")
    return rslt

def createOtherPolicy(rslt):
    rslt = rslt + jumptab(2, 1) + "Policies:"
    rslt = rslt + jumptab(1, 2) + "Readers:"
    rslt = rslt + jumptab(1, 3) + "Type: ImplicitMeta"
    rslt = rslt + jumptab(1, 3) + "Rule: \"ANY Readers\""
    rslt = rslt + jumptab(1, 2) + "Writers:"
    rslt = rslt + jumptab(1, 3) + "Type: ImplicitMeta"
    rslt = rslt + jumptab(1, 3) + "Rule: \"ANY Writers\""
    rslt = rslt + jumptab(1, 2) + "Admins:"
    rslt = rslt + jumptab(1, 3) + "Type: ImplicitMeta"
    rslt = rslt + jumptab(1, 3) + "Rule: \"MAJORITY Admins\""
    return rslt

#Part of configtx.yaml
def createOrderer(typeorderer, messageCount, absoluteMaxBytes, preferredMaxBytes, host, policy="OR"):
    rslt = jumptab(2, 0) + "Orderer: &OrdererDefaults"
    rslt += jumptab(2, 1) + "OrdererType: " + typeorderer
    rslt += jumptab(2, 1) + "Addresses:"
    rslt += jumptab(1, 2) + "- " + "orderer." + host + ".com:7050"
    rslt += jumptab(2, 1) + "BatchTimeout: 2s"
    rslt += jumptab(2, 1) + "BatchSize:"
    rslt += jumptab(2, 2) + "MaxMessageCount: " + messageCount
    rslt += jumptab(1, 2) + "AbsoluteMaxBytes: " + absoluteMaxBytes
    rslt += jumptab(1, 2) + "PreferredMaxBytes: " + preferredMaxBytes
    rslt += jumptab(2, 1) + "Kafka:"
    rslt += jumptab(1, 2) + "Brokers:"
    rslt += jumptab(1, 3) + "- 127.0.0.1:9092"
    rslt += jumptab(2, 1) + "Organizations:"

    #Policy
    #rslt = createOtherPolicy(rslt)
    #rslt = rslt + jumptab(1, 2) + "BlockValidation:"
    #rslt = rslt + jumptab(1, 3) + "Type: ImplicitMeta"
    #rslt = rslt + jumptab(1, 3) + "Rule: ANY Writers"
    return (rslt)


#Part of configtx.yaml
def setOrg(tab):
    rslt = jumptab(2, 0) + createOrganisations("OrdererOrg", 0, tab[0])
    i = 2
    while (i < len(tab)):
        rslt += jumptab(2, 0) + createOrganisations(tab[i], 1, tab[0])
        i += 2
    return (rslt)

#Call functions in order to create crypto-config.yaml
def createCryptoconfig(tab):
    buffer = ordererOrgConfig(tab[0])
    buffer += jumptab(2, 0) + "PeerOrgs:"
    i = 2
    while (i < len(tab)):
        buffer += jumptab(2, 1) + "- Name: " + tab[i]
        buffer += jumptab(1, 1) + "  Domain: " + tab[i] + "." + tab[0] + ".com"
        buffer += jumptab(1, 1) + "  EnableNodeOUs: true"
        buffer += jumptab(2, 2) + "Template:"
        buffer += jumptab(1, 3) + "Count: " + tab[i + 1]
        buffer += jumptab(2, 2) + "Users:"
        buffer += jumptab(1, 3) + "Count: {0}".format(int(tab[i + 1])-1 if int(tab[i + 1])-1 > 1 else 1)
        i += 2
    return (buffer)
##############################################################################################################################
#Part of crypto-config.yaml - OrdererOrgs section
def ordererOrgConfig(host):
    rslt = "OrdererOrgs:"
    rslt += jumptab(2, 1) + "- Name: Orderer"
    rslt += jumptab(1, 1) + "  Domain: " + host + ".com"
    rslt += jumptab(2, 2) + "Specs:"
    rslt += jumptab(1, 3) + "- Hostname: orderer"
    return (rslt)

#Call functions in order to create configtx.yaml
def createConfigtx(tabName):
    buffer = "Organizations:"
    buffer += setOrg(tabName)
    #buffer += jumptab(2,0) + createCapabilities()
    buffer += createOrderer("solo", "10", "98 MB", "512 KB", tabName[0])
    buffer += jumptab(2, 0) + "Application: &ApplicationDefaults"
    buffer += jumptab(2, 1) + "Organizations:"
    res = ""
    #buffer += jumptab(1, 2) + createOtherPolicy(res)
    #buffer += jumptab(2, 0) + createChannelConfigtx()
    buffer += jumptab(2, 0) + "Profiles:"
    buffer += jumptab(2, 0) + createProfiles(tabName, "ProfileTest", "OrdererOrg")
    buffer += jumptab(2, 0) + createChannelProfile(tabName, "ChannelTest")
    return (buffer) 



#Ask user for network mapping
def getArg():
    orgName = [input("Your network name : ")]
    orgName.append(input("Your first channel name : "))
    orgName.append(input("First org name : "))
    orgName.append(str(getNumber()))
    while (input("Do you want to create another organisation ? (y/N) ") == 'y' ):
        name = ""
        while sameName(orgName, name) == 0:
            if (name != ""):
                print("Name already used by another org")
            name = input("New org name : ")
        orgName.append(name)
        orgName.append(str(getNumber()))
    return (orgName)

#Get number of peer
def getNumber():
    peerNb = -1
    while peerNb < 0:
        while True:
            try:
                peerNb = int(input("Number of peer : "))
                break
            except:
                print("Please enter a number")
        if peerNb < 0:
            print("Please enter a positive number")
    return (peerNb)

#Error handling
def sameName(tab, name):
    i = 2
    if name == "":
        return (0)
    while i < len(tab):
        if tab[i] == name:
            return (0)
        i += 2
    return (1)

#Docker-compose.yaml header
def headerDockerFile(tab):
    rslt = "version: '2'"
    rslt += jumptab(2,0) + "networks:"
    rslt += jumptab(1, 1) + tab[0] + ":"
    rslt += jumptab(1, 1) + volumeDockerFile(tab)
    rslt += jumptab(2, 0) + "services:"
    return (rslt)

#Part of docker-compose.yaml - CA section
def caDockerFile(arch, hostname, rank, network):
    rslt = jumptab(2, 1) + "ca." + hostname + ":"
    rslt += jumptab(1, 2) + "image: hyperledger/fabric-ca:$IMAGE_TAG"
    rslt += jumptab(1, 2) + "environment:"
    rslt += jumptab(1, 3) + "- FABRIC_CA_HOME=/etc/hyperledger/fabric-ca-server"
    rslt += jumptab(1, 3) + "- FABRIC_CA_SERVER_CA_NAME=ca." + hostname
    rslt += list_value("FABRIC_CA_SERVER_TLS_ENABLED=true")
    rslt += list_value("FABRIC_CA_SERVER_TLS_CERTFILE=/etc/hyperledger/fabric-ca-server-config/ca."+hostname+"-cert.pem")
    rslt += list_value("FABRIC_CA_SERVER_TLS_KEYFILE=/etc/hyperledger/fabric-ca-server-config/CA"+hostname+"_PRIVATE_KEY")

    rslt += jumptab(1, 2) + "ports:"
    rslt += jumptab(1, 3) + "- \"" + str((7 + rank)) + "054:7054\""
    rslt += jumptab(1, 2) + "command: sh -c 'fabric-ca-server start --ca.certfile /etc/hyperledger/fabric-ca-server-config/ca." + hostname + "-cert.pem --ca.keyfile /etc/hyperledger/fabric-ca-server-config/CA"+ hostname+"_PRIVATE_KEY -b admin:adminpw -d'"
    rslt += jumptab(1, 2) + "volumes:"
    rslt += jumptab(1, 3) + "- ./crypto-config/peerOrganizations/" + hostname + "/ca/:/etc/hyperledger/fabric-ca-server-config"
    rslt += jumptab(1, 2) + "container_name: ca." + hostname
    rslt += jumptab(1, 2) + "networks:"
    rslt += jumptab(1, 3) + "- " + network
    return (rslt)

#Useful function for create docker-compose.yaml
def container_name(value):
    return (jumptab(1, 2) + "container_name: " + value)

#Useful function for create docker-compose.yaml
def image(value):
    return (jumptab(1, 2) + "image: " + value)

#Useful function for create docker-compose.yaml
def working_dir(value):
    return (jumptab(1, 2) + "working_dir: " + value)

#Useful function for create docker-compose.yaml
def command(value):
    return (jumptab(1, 2) + "command: " + value)

#Useful function for create docker-compose.yaml
def list_value(value):
    return (jumptab(1, 3) + "- " + value)

#Part of docker-compose.yaml - Zookeeper section
def zookeeperDockerFile(network, rank):
    rslt = jumptab(2, 1) + "zookeeper" + str(rank) + ":"
    rslt += container_name("zookeeper" + str(rank))
    rslt += jumptab(1, 2) + "extends:"
    rslt += jumptab(1, 4) + "file: docker-compose-base.yml"
    rslt += jumptab(1, 4) + "service: zookeeper"
    rslt += jumptab(1, 2) + "environment:"
    rslt += list_value("ZOO_MY_ID=" + str((rank + 1)))
    rslt += list_value("ZOO_SERVERS=server.1=zookeeper0:2888:3888 server.2=zookeeper1:2888:3888 server.3=zookeeper2:2888:3888")
    rslt += jumptab(1, 2) + "networks:"
    rslt += list_value(network)
    return (rslt)

#Part of docker-compose.yaml - Kafka section
def kafkaDockerFile(network, rank):
    rslt = jumptab(2, 1) + "kafka" + str(rank) + ":"
    rslt += container_name("kafka" + str(rank))
    rslt += jumptab(1, 2) + "extends:"
    rslt += jumptab(1, 4) + "file: docker-compose-base.yml"
    rslt += jumptab(1, 4) + "service: kafka"
    rslt += jumptab(1, 2) + "environment:"
    rslt += list_value("KAFKA_BROKER_ID=" + str(rank))
    rslt += list_value("KAFKA_ZOOKEEPER_CONNECT=zookeeper0:2181,zookeeper1:2181,zookeeper2:2181")
    rslt += list_value("KAFKA_MESSAGE_MAX_BYTES=103809024")
    rslt += list_value("KAFKA_REPLICA_FETCH_MAX_BYTES=103809024")
    rslt += list_value("KAFKA_REPLICA_FETCH_RESPONSE_MAX_BYTES=103809024")
    rslt += jumptab(1, 2) + "depends_on:"
    rslt += list_value("zookeeper0")
    rslt += list_value("zookeeper1")
    rslt += list_value("zookeeper2")
    rslt += jumptab(1, 2) + "networks:"
    rslt += list_value(network)
    return (rslt)

#Part of docker-compose.yaml - Orderer section
def ordererDockerFile(hostname, rank, network, arch):
    rslt = jumptab(2, 1) + "orderer." + hostname + ":"
    rslt += container_name("orderer." + hostname)
    rslt += image("hyperledger/fabric-orderer:$IMAGE_TAG")
    rslt += working_dir("/opt/gopath/src/github.com/hyperledger/fabric")
    rslt += command("orderer")
    #env
    rslt += jumptab(1, 2) + "environment:"
    rslt += list_value("ORDERER_GENERAL_LOGLEVEL=DEBUG")
    rslt += list_value("ORDERER_GENERAL_LISTENADDRESS=0.0.0.0")
    rslt += list_value("ORDERER_GENERAL_GENESISMETHOD=file")
    rslt += list_value("ORDERER_GENERAL_GENESISFILE=/var/hyperledger/orderer/orderer.genesis.block")
    rslt += list_value("ORDERER_GENERAL_LOCALMSPID=OrdererMSP")
    rslt += list_value("ORDERER_GENERAL_LOCALMSPDIR=/var/hyperledger/orderer/msp")
    #tls env
    rslt += list_value("ORDERER_GENERAL_TLS_ENABLED=true")
    rslt += list_value("ORDERER_GENERAL_TLS_PRIVATEKEY=/var/hyperledger/orderer/tls/server.key")
    rslt += list_value("ORDERER_GENERAL_TLS_CERTIFICATE=/var/hyperledger/orderer/tls/server.crt")
    rslt += list_value("ORDERER_GENERAL_TLS_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]")
    rslt += jumptab(1, 2) + "ports:"
    rslt += list_value(str((7 + rank)) + "050:7050")
    rslt += jumptab(1, 2) + "volumes:"
    rslt += list_value("./channel-artifacts/genesis.block:/var/hyperledger/orderer/orderer.genesis.block")
    rslt += list_value("./crypto-config/ordererOrganizations/" + hostname + "/orderers/" + "orderer." + hostname +  "/msp:/var/hyperledger/orderer/msp")
    rslt += list_value("./crypto-config/ordererOrganizations/" + hostname + "/orderers/" + "orderer." + hostname +  "/tls:/var/hyperledger/orderer/tls")
    rslt += list_value("orderer."+ hostname +":/var/hyperledger/production/orderer")
    #rslt += list_value("./config/:/etc/hyperledger/configtx")

    rslt += jumptab(1, 2) + "networks:"
    rslt += list_value(network)
    return (rslt)

#Part of docker-compose.yaml - Coucdh section
def couchDBDockerFile(arch, network, rank):
    rslt = jumptab(2, 1) + "couchdb" + str(rank) + ":"
    rslt += container_name("couchdb" + str(rank))
    rslt += image("hyperledger/fabric-couchdb:$IMAGE_TAG")
    rslt += jumptab(1, 2) + "ports:"
    rslt += list_value(str((rank + 5)) + "984:5984")
    rslt += jumptab(1, 2) + "environment:"
    rslt += jumptab(1, 3) + "- COUCHDB_USER="
    rslt += jumptab(1, 3) + "- COUCHDB_PASSWORD="
    rslt += jumptab(1, 2) + "networks:"
    rslt += list_value(network)
    return (rslt)

#Part of docker-compose.yaml - Peer section
def peerDockerFile(hostname, rank, network, arch, idd, name):
    rslt = jumptab(2, 1) + "peer" + str(idd) + "." + hostname + ":"
    rslt += container_name("peer" + str(idd) + "." + hostname)
    rslt += working_dir("/opt/gopath/src/github.com/hyperledger/fabric/peer")
    #rslt += jumptab(1, 2) + "extends:"
    #rslt += jumptab(1, 3) + "file: docker-compose-base.yml"
    #rslt += jumptab(1, 3) + "service: peer"

    rslt += image("hyperledger/fabric-peer:$IMAGE_TAG")
    rslt += command("peer node start")

    rslt += jumptab(1, 2) + "environment:"

    rslt += list_value("CORE_PEER_ID=peer" + str(idd) + "." + hostname)
    rslt += list_value("CORE_PEER_ADDRESS=peer" + str(idd) + "." + hostname + ":7051")
    rslt += list_value("CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer" + str(idd) + "." + hostname + ":7051")
    rslt += list_value("CORE_PEER_GOSSIP_BOOTSTRAP=peer" + str(idd-1 if idd-1 >= 0 else idd+1) + "." + hostname + ":7051")
    rslt += list_value("CORE_PEER_LOCALMSPID=" + name + "MSP")

    rslt += list_value("CORE_LOGGING_LEVEL=DEBUG")
    rslt += list_value("CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock")
    rslt += list_value("CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=hyperledger-fabric-automate-installer_"+network)

    rslt += list_value("CORE_LEDGER_STATE_STATEDATABASE=CouchDB")
    rslt += list_value("CORE_LEDGER_STATE_COUCHDBCONFIG_COUCHDBADDRESS=couchdb" + str(rank) + ":5984")
    rslt += list_value("CORE_LEDGER_STATE_COUCHDBCONFIG_USERNAME=")
    rslt += list_value("CORE_LEDGER_STATE_COUCHDBCONFIG_PASSWORD=")

    rslt += list_value("CORE_PEER_TLS_ENABLED=true")
    rslt += list_value("CORE_PEER_GOSSIP_USELEADERELECTION=true")
    rslt += list_value("CORE_PEER_GOSSIP_ORGLEADER=false")
    rslt += list_value("CORE_PEER_PROFILE_ENABLED=true")
    rslt += list_value("CORE_PEER_TLS_CERT_FILE=/etc/hyperledger/fabric/tls/server.crt")
    rslt += list_value("CORE_PEER_TLS_KEY_FILE=/etc/hyperledger/fabric/tls/server.key")
    rslt += list_value("CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/fabric/tls/ca.crt")


    rslt += jumptab(1, 2) + "ports:"
    rslt += list_value(str((7 + rank)) + "051:7051")
    rslt += list_value(str((7 + rank)) + "053:7053")

    rslt += jumptab(1, 2) + "volumes:"
    rslt += list_value("/var/run/:/host/var/run/")
    rslt += list_value("./crypto-config/peerOrganizations/" + hostname + "/peers/peer" + str(idd) + "." + hostname + "/msp:/etc/hyperledger/fabric/msp")
    rslt += list_value("./crypto-config/peerOrganizations/" + hostname + "/peers/peer" + str(idd) + "." + hostname + "/tls:/etc/hyperledger/fabric/tls")
    rslt += list_value("peer"+str(idd)+"." + hostname + ":/var/hyperledger/production")
    #rslt += list_value("./config/:/etc/hyperledger/configtx")


    rslt += jumptab(1, 2) + "depends_on:"
    if (arch != "test"):
        rslt += list_value("orderer." + network + ".com")
    rslt += list_value("couchdb" + str(rank))
    rslt += jumptab(1, 2) + "networks:"
    rslt += list_value(network)
    return (rslt)

def cliDockerFile(tab):

    network = tab[0]
    org = tab[2]
    rslt = "cli:"
    rslt += jumptab(1,2) + "container_name: cli"
    rslt += jumptab(1, 2) + "image: hyperledger/fabric-tools:$IMAGE_TAG"
    rslt += jumptab(1, 2) + "tty: true"
    rslt += jumptab(1, 2) + "stdin_open: true"
    rslt += jumptab(1, 2) + "environment:"
    rslt += list_value("GOPATH=/opt/gopath")
    rslt += list_value("CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock")
    rslt += list_value("CORE_LOGGING_LEVEL=INFO")
    rslt += list_value("CORE_PEER_ID=cli")
    rslt += list_value("CORE_PEER_ADDRESS=peer0."+ org +"." +network +".com:7051")
    rslt += list_value("CORE_PEER_LOCALMSPID="+org+"MSP")
    rslt += list_value("CORE_PEER_TLS_ENABLED=true")
    rslt += list_value("CORE_PEER_TLS_CERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/{0}.{1}.com/peers/peer0.{0}.{1}.com/tls/server.crt".format(org, network))
    rslt += list_value("CORE_PEER_TLS_KEY_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/{0}.{1}.com/peers/peer0.{0}.{1}.com/tls/server.key".format(org, network))
    rslt += list_value("CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/{0}.{1}.com/peers/peer0.{0}.{1}.com/tls/ca.crt".format(org, network))
    rslt += list_value("CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/{0}.{1}.com/users/Admin@{0}.{1}.com/msp".format(org, network))
    #rslt += list_value("CORE_CHAINCODE_KEEPALIVE=10")

    rslt += jumptab(1, 2) + "working_dir: /opt/gopath/src/github.com/hyperledger/fabric/peer"
    rslt += jumptab(1, 2) + "command: /bin/bash"
    rslt += jumptab(1, 2) + "volumes:"
    rslt += list_value("/var/run/:/host/var/run/")
    rslt += list_value("./chaincode/:/opt/gopath/src/github.com/chaincode")
    rslt += list_value("./crypto-config:/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/")
    rslt += list_value("./scripts:/opt/gopath/src/github.com/hyperledger/fabric/peer/scripts/")
    rslt += list_value("./channel-artifacts:/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts")

    rslt += jumptab(1, 2) + "depends_on:"
    rslt += list_value("orderer.{0}.com".format(network))

    for k in range(2,len(tab),2):
        for j in range(0,int(tab[k+1])):
            rslt += list_value("peer{0}.{1}.{2}.com".format(j,tab[k], network))

    rslt += jumptab(1, 2) + "networks:"
    rslt += list_value(network)

    return rslt

def volumeDockerFile(tab):
    res = jumptab(1, 0) + "volumes:"
    print(tab)
    res += jumptab(1, 1) + "orderer."+tab[0]+".com:"
    for k in range(2, len(tab), 2):
        for j in range(0, int(tab[k+1])):
            res += jumptab(1, 1) + "peer"+str(j)+"."+tab[k]+"."+tab[0]+".com:"

    return res

#Call functions in order to create docker-composer.yaml
def createDockerFile(tab):
    network = tab[0]
    arch = tab[1]
    orgNB = int((len(tab) - 2) / 2)
    buffer = headerDockerFile(tab)
    buffer += ordererDockerFile(network + ".com", 0, network, "$ARCH")

    rank = 0
    index = 3
    for k in range (0, orgNB):
        buffer += caDockerFile("$ARCH", tab[index - 1] + "." + network + ".com", k, network)
        for i in range (0, int(tab[index])):
            buffer += peerDockerFile(tab[index - 1] + "." + network + ".com", rank, network, "$ARCH", i, tab[index - 1])
            buffer += couchDBDockerFile("$ARCH", network, rank)
            rank += 1
        index += 2

    buffer += jumptab(2, 1) + cliDockerFile(tab)
    return (buffer)

#Part of launch.sh
def createGenNeeded(channelId, tab):
    orgNB = int((len(tab) - 2) / 2)
    index = 2
    rslt = "function gen_needed(){\n\tmkdir channel-artifacts\n\texport CHANNEL_NAME=" + channelId + "\n\texport FABRIC_CFG_PATH=$PWD\n\t./bin/cryptogen generate --config=./crypto-config.yaml\n\t./bin/configtxgen -profile ProfileTest -outputBlock ./channel-artifacts/genesis.block \n"#-channelID $CHANNEL_NAME\n"
    rslt += "\t./bin/configtxgen -profile ChannelTest -outputCreateChannelTx ./channel-artifacts/channel.tx   -channelID " + channelId
    for i in range (0, orgNB):
        rslt += jumptab(1, 0) + "\t./bin/configtxgen -profile ChannelTest -outputAnchorPeersUpdate ./channel-artifacts/" + tab[index] + "MSPanchors.tx -channelID " + channelId + " -asOrg " + tab[index] +"MSP"
        index += 2
    rslt += "\n"
    rslt += "}\n"
    return (rslt)

#Part of launch.sh
def createConst():
    rslt = "function clean_it() {\n\tdocker-compose -f docker-compose.yaml down --volumes --remove-orphans\n\tdocker rm $(docker ps -aq)\n\trm -rf crypto-config/*\n\trm -rf channel-artifacts/*\n}\n\nfunction start_network() {\n\tdocker-compose -f docker-compose.yaml up -d\n}\n\n" \
           "MODE=$1" \
           "" \
           "clean_it\ngen_needed\nreplace_key\nstart_network"
    return (rslt)

#Part of launch.sh
def createJoinChannel(tab, channelId):
    index = 3
    orgNB = int((len(tab) - 2) / 2)
    #create channel
    #"docker exec peer0." + tab[2] + "." + tab[0] + ".com peer channel create -o orderer." + tab[0] + ".com:7050 -c " + channelId + " -f /etc/hyperledger/configtx/channel.tx --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA"
    rslt = "function join_channel() {\n\techo \"Channel "+  channelId + " creation ...\"\n\t"
    rslt += set_globals(index, tab)

    rslt += core_peer_address(0, index, tab)
    rslt += "\n\tpeer channel create -o orderer." + tab[0] + ".com:7050 -c " + channelId + " -f ./channel-artifacts/channel.tx --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA\n"

    for i in range(0, orgNB):
        rslt += jumptab(1,1) + set_globals(index, tab)
        #rslt += jumptab(1, 0) + "\tdocker exec peer0." + tab[2] + "." + tab[0] + ".com cp " + channelId + ".block /etc/hyperledger/configtx"
        for k in range (0, int(tab[index])):
            rslt += jumptab(1, 0) + "\tsleep 3"
            rslt += jumptab(1, 0) + core_peer_address(k, index, tab)
            rslt += jumptab(1, 0) + "\tpeer channel join -b " + channelId + ".block\n"
        index += 2
    rslt += "\n}"
    return (rslt)


def core_peer_address(k,index, tab):
    return "\n\tCORE_PEER_ADDRESS=peer"+str(k)+"." + tab[index - 1] + "." + tab[0] + ".com:7051"


def createUpdateAnchorPeer(tab, channelId):
    index = 3
    orgNB = int((len(tab) - 2) / 2)

    rslt = "function update_anchorpeer() {\n\techo \"Update Anchor peer ...\""
    for i in range (0, orgNB):
        rslt += jumptab(1,1) + "echo \"Update Anchor peer" + tab[index-1] + "MSP ...\""
        rslt += jumptab(1,1) + set_globals(index, tab)
        rslt += jumptab(1,1) + core_peer_address(0, index, tab)
        rslt += jumptab(1,1) + "peer channel update -o orderer." + tab[0] + ".com:7050 -c " + channelId + " -f ./channel-artifacts/${CORE_PEER_LOCALMSPID}anchors.tx --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA"
        index += 2
    rslt += "\n}"
    return rslt

def createInstallChaincode(tab, channelId):
    index = 3
    orgNB = int((len(tab) - 2) / 2)

    rslt = "function install_chaincode() {\n\techo \"Install chaincode ...\""
    rslt += jumptab(1, 1) + "VERSION=${3:-1.0}"
    for i in range(0, orgNB):
        rslt += jumptab(2, 1) + "echo \"Install chaincode in peer0." + tab[index - 1] + ".com...\""
        rslt += set_globals(index, tab)
        rslt += core_peer_address(0, index, tab)
        rslt += jumptab(1, 1) + "peer chaincode install -n mycc -v ${VERSION} -l node -p ${CC_SRC_PATH}"
        index += 2

    rslt += "\n}"
    return rslt

def createInstantiateChaincode(tab, channelId):
    index = 3
    orgNB = int((len(tab) - 2) / 2)

    rslt = "function instantiate_chaincode() {\n\techo \"Instantiate chaincode ...\""
    rslt += jumptab(1, 2) + "VERSION=${3:-1.0}"
    rslt += jumptab(2, 2) + "echo \"Instantiate chaincode in peer0." + tab[index - 1] + ".com...\""
    rslt += set_globals(index, tab)
    rslt += core_peer_address(0, index, tab)
    args = '\'{"Args":["init","a","100","b","200"]}\'' #TODO pass it at the beginning

    pol = "\"AND (" #TODO pass it?
    pol += "'"+tab[index-1]+"MSP.peer'"
    index += 2
    for i in range(1, orgNB):
        pol += ","
        pol += "'" + tab[index - 1] + "MSP.peer'"
        index += 2

    pol += ")\""
    rslt += jumptab(1, 2) + "peer chaincode instantiate -o orderer.example.com:7050 --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA -C " + channelId + " -n mycc -v ${VERSION} -l node -c " + args + " -P " + pol

    rslt += "\n}"
    return rslt

def createQueryChaincode(tab, channelId, result):
    index = 5
    orgNB = int((len(tab) - 2) / 2)
    rslt = "function query_chaincode() {\n\techo \"Querying chaincode ...\""
    rslt += jumptab(2, 2) + "echo \"Querying chaincode in peer0." + tab[index - 1] + ".example.com...\""
    rslt += set_globals(index, tab)
    rslt += core_peer_address(0, index, tab)
    args = '\'{"Args":["query","a"]}\''
    rslt += jumptab(1, 2) + "peer chaincode query -C "+ channelId +" -n mycc -c "+args
    rslt += "\n}"
    return rslt

def set_globals(index, tab):
    rslt = "\n\tCORE_PEER_LOCALMSPID=" + tab[index - 1] + "MSP" \
            "\n\tCORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/" + tab[index - 1] + "." + tab[0] + ".com/peers/peer0." + tab[index - 1] + "." + tab[0] + ".com/tls/ca.crt" \
            "\n\tCORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/" +tab[index - 1] + "." + tab[0] + ".com/users/Admin@" + tab[index - 1] + "." + tab[0] + ".com/msp" \
        # rslt += jumptab(1, 0) + "\tcp " + channelId + ".block /etc/hyperledger/configtx"
    return rslt


def createReplaceKey(tab):
    index = 2
    orgNB = int((len(tab) - 2) / 2)
    # create channel
    rslt = "function replace_key() {" \
           "\n\techo \"Replacing key...\"" \
           "\n\tCURRENT_DIR=$PWD" \

    for i in range(0, orgNB):
        rslt += "\n\tcd crypto-config/peerOrganizations/"+tab[index]+"."+tab[0]+".com/ca" \
                    "\n\tPRIV_KEY=$(ls *_sk)" \
                    "\n\tcd $CURRENT_DIR" \
                    "\n\tsed -i \"s/CA"+ tab[index] + "." + tab[0]+ ".com_PRIVATE_KEY/${PRIV_KEY}/g\" docker-compose.yaml"
        index += 2
    rslt += "\n}"
    return rslt

#Call functions in order to create launch.sh
def createScript(tab):
    buffer = "#!/bin/bash"
    buffer += const_variables
    buffer += jumptab(2, 0) + createGenNeeded(tab[1], tab)
    buffer += jumptab(2, 0) + createReplaceKey(tab)
    #buffer += jumptab(2, 0) + createJoinChannel(tab, tab[1])

    buffer += jumptab(2, 0) + createConst()
    buffer += jumptab(1, 0) + "sed -i -e 's/\\r$//' scripts/script.sh"
    buffer += jumptab(1, 0) + "docker exec cli scripts/script.sh"
    return (buffer)

def createScriptCli(tab):
    buffer = "#!/bin/bash"
    buffer += jumptab(1,0) + "export ORDERER_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/"+ tab[0] + ".com/orderers/orderer."+ tab[0] + ".com/msp/tlscacerts/tlsca."+ tab[0] + ".com-cert.pem"
    buffer += jumptab(1,0) + "export CC_SRC_PATH=/opt/gopath/src/github.com/chaincode/"
    buffer += jumptab(2, 0) + createJoinChannel(tab, tab[1])
    buffer += jumptab(2, 0) + createUpdateAnchorPeer(tab, tab[1])

    buffer += jumptab(2, 0) + createInstallChaincode(tab, tab[1])
    buffer += jumptab(2, 0) + createInstantiateChaincode(tab, tab[1])
    buffer += jumptab(2, 0) + createQueryChaincode(tab, tab[1], 100)


    buffer += jumptab(1, 0) +"sleep 10\njoin_channel\nupdate_anchorpeer\ninstall_chaincode\ninstantiate_chaincode\nquery_chaincode"
    return buffer

#Main function
def createNewOrg():
    tab = getArg()
    script = open("launch.sh", "w")
    scriptBuffer = createScript(tab)
    script.write(scriptBuffer)
    script.close()
    script = open("scripts/script.sh", "w")
    scriptBuffer = createScriptCli(tab)
    script.write(scriptBuffer)
    script.close()
    dockerCompose = open("docker-compose.yaml", "w")
    cryptoConfig = open("crypto-config.yaml", "w")
    configtx = open("configtx.yaml", "w")
    composeBuffer = createDockerFile(tab)
    cryptoBuffer = createCryptoconfig(tab)
    configtxBuffer = createConfigtx(tab)
    dockerCompose.write(composeBuffer)
    dockerCompose.close()
    cryptoConfig.write(cryptoBuffer)
    cryptoConfig.close()
    configtx.write(configtxBuffer)
    configtx.close()


createNewOrg()
