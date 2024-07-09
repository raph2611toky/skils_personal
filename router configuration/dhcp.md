DHCP CLIENT
-----------
Configuration de router pour attribuer des addresses ip par dhcp au client,

>enable

R1#sh ip int brief
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            unassigned      YES unset  administratively down down
Ethernet1/0                192.168.1.1     YES manual up                    up  
Ethernet1/1                192.168.2.1     YES manual up                    up  



R1#conf t                                               # configure terminal
R1(config)#int e1/1                                     # choisir l'interface de source de dhcp
R1(config-if)#ip dhcp pool client                       # nom du plage de piscine dhcp
R1(dhcp-config)#network 192.168.2.0 255.255.255.0       # addresse reseau du partage dhcp et son mask
R1(dhcp-config)#default-router 192.168.2.1              # le passerelle de dhcp
R1(dhcp-config)#lease infinite
R1(dhcp-config)#ip dhcp excluded-address 192.168.2.1
R1(config)#
