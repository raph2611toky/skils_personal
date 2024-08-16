D'accord, voici la configuration mise à jour avec la topologie RIP modifiée et les détails complets pour le routage dynamique dans GNS3.

## Configuration des Protocoles de Routage dans GNS3

### 1. Configuration DHCP

#### Attribution d'Adresse IP via Routeur

1. **Configurer le Routeur pour le DHCP :**

   ```bash
   R1# configure terminal
   R1(config)# ip dhcp pool CLIENT
   R1(dhcp-config)# network 192.168.2.0 255.255.255.0
   R1(dhcp-config)# default-router 192.168.2.1
   R1(dhcp-config)# lease infinite
   R1(dhcp-config)# ip dhcp excluded-address 192.168.2.1
   R1(config)# end
   ```

#### Attribution d'Adresse IP via Serveur DHCP

1. **Configurer un Serveur DHCP (si nécessaire) :**

   ```bash
   DHCP_SERVER# configure terminal
   DHCP_SERVER(config)# ip dhcp pool SERVER_POOL
   DHCP_SERVER(dhcp-config)# network 192.168.10.0 255.255.255.0
   DHCP_SERVER(dhcp-config)# default-router 192.168.10.1
   DHCP_SERVER(dhcp-config)# lease 7
   DHCP_SERVER(config)# end
   ```

### 2. Configuration DNS

1. **Configurer le DNS sur le Routeur :**

   ```bash
   ROUTER# configure terminal
   ROUTER(config)# ip name-server 8.8.8.8
   ROUTER(config)# end
   ```

### 3. Configuration des Routeurs pour l'Accès à Internet

#### NAT Inside et Outside

1. **Configurer NAT sur le Routeur :**

   ```bash
   ROUTER# configure terminal
   ROUTER(config)# interface FastEthernet0/0
   ROUTER(config-if)# ip address 192.168.1.1 255.255.255.0
   ROUTER(config-if)# ip nat inside
   ROUTER(config-if)# no shutdown
   ROUTER(config)# interface Serial0/0
   ROUTER(config-if)# ip address 203.0.113.1 255.255.255.0
   ROUTER(config-if)# ip nat outside
   ROUTER(config-if)# no shutdown
   ROUTER(config)# ip nat inside source list 1 interface Serial0/0 overload
   ROUTER(config)# access-list 1 permit 192.168.1.0 0.0.0.255
   ROUTER(config)# end
   ```

### 4. Configuration du Routage Statique

1. **Configurer le Routage Statique entre deux Routeurs :**

   - **Routeur 1 :**

     ```bash
     R1# configure terminal
     R1(config)# ip route 10.0.0.0 255.255.255.0 192.168.1.2
     R1(config)# end
     ```

   - **Routeur 2 :**

     ```bash
     R2# configure terminal
     R2(config)# ip route 192.168.1.0 255.255.255.0 10.0.0.1
     R2(config)# end
     ```

### 5. Configuration du Routage Dynamique

#### Routage RIP

##### Topologie RIP

La topologie RIP est un hexagone avec les liaisons suivantes : R1-R2, R2-R3, R3-R4, R4-R5, R5-R6, R6-R1.

```
         R2 ----------- R3
        /                  \
      /                      \
    R1                       R4
      \                      /
        \                  /
         R6 ----------- R5
```

##### Configuration des Routeurs RIP

1. **Configurer R1 :**

   ```bash
   R1# configure terminal
   R1(config)# router rip
   R1(config-router)# version 2
   R1(config-router)# network 192.168.1.0
   R1(config-router)# network 192.168.2.0
   R1(config-router)# no auto-summary
   R1(config)# end
   ```

2. **Configurer R2 :**

   ```bash
   R2# configure terminal
   R2(config)# router rip
   R2(config-router)# version 2
   R2(config-router)# network 192.168.1.0
   R2(config-router)# network 192.168.3.0
   R2(config-router)# no auto-summary
   R2(config)# end
   ```

3. **Configurer R3 :**

   ```bash
   R3# configure terminal
   R3(config)# router rip
   R3(config-router)# version 2
   R3(config-router)# network 192.168.2.0
   R3(config-router)# network 192.168.4.0
   R3(config-router)# no auto-summary
   R3(config)# end
   ```

4. **Configurer R4 :**

   ```bash
   R4# configure terminal
   R4(config)# router rip
   R4(config-router)# version 2
   R4(config-router)# network 192.168.3.0
   R4(config-router)# network 192.168.5.0
   R4(config-router)# no auto-summary
   R4(config)# end
   ```

5. **Configurer R5 :**

   ```bash
   R5# configure terminal
   R5(config)# router rip
   R5(config-router)# version 2
   R5(config-router)# network 192.168.4.0
   R5(config-router)# network 192.168.6.0
   R5(config-router)# no auto-summary
   R5(config)# end
   ```

6. **Configurer R6 :**

   ```bash
   R6# configure terminal
   R6(config)# router rip
   R6(config-router)# version 2
   R6(config-router)# network 192.168.5.0
   R6(config-router)# network 192.168.6.0
   R6(config-router)# no auto-summary
   R6(config)# end
   ```

#### Routage OSPF

##### Topologie OSPF

La topologie OSPF est un triangle avec les liaisons suivantes : R8-R9, R9-R10, R10-R8.

```
    R8
   /  \
  R9----R10
```

##### Configuration des Routeurs OSPF

1. **Configurer R8 :**

   ```bash
   R8# configure terminal
   R8(config)# router ospf 1
   R8(config-router)# network 10.0.0.0 0.0.0.255 area 0
   R8(config)# end
   ```

2. **Configurer R9 :**

   ```bash
   R9# configure terminal
   R9(config)# router ospf 1
   R9(config-router)# network 10.0.0.0 0.0.0.255 area 0
   R9(config)# end
   ```

3. **Configurer R10 :**

   ```bash
   R10# configure terminal
   R10(config)# router ospf 1
   R10(config-router)# network 10.0.0.0 0.0.0.255 area 0
   R10(config)# end
   ```

#### Connexion entre RIP et OSPF

Pour connecter un routeur de RIP (R4) à un routeur d'OSPF (R8), nous utiliserons la redistribution de routes.

1. **Configurer la Redistribution sur R4 :**

   ```bash
   R4# configure terminal
   R4(config)# router rip
   R4(config-router)# redistribute ospf 1
   R4(config-router)# end
   ```

2. **Configurer la Redistribution sur R8 :**

   ```bash
   R8# configure terminal
   R8(config)# router ospf 1
   R8(config-router)# redistribute rip
   R8(config)# end
   ```

3. **Configurer les Interfaces :**

   Assurez-vous que les interfaces entre les routeurs RIP et OSPF sont correctement configurées avec des adresses IP.

   - **Configurer les Interfaces de R4 :**

     ```bash
     R4# configure terminal
     R4(config)# interface FastEthernet0/1
     R4(config-if)# ip address 192.168.4.1 255.255.255.0
     R4(config-if)# no shutdown
     R4(config)# end
     ```

   - **Configurer les Interfaces de R8 :**

     ```bash
     R8# configure terminal
     R8(config)# interface FastEthernet0/1
     R8(config-if)# ip address 10.0.0.1 255.255.255.0
     R8(config-if)# no shutdown
     R8(config)# end
     ```

4. **Vérifiez les Tables de Routage :**

   Sur R4, vous devriez voir les routes OSPF dans la table RIP et inversement sur R8.

   - **Sur R4 :**

     ```bash
     R4# show ip route rip
     ```

   - **Sur R8 :**

     ```bash
    

 R8# show ip route ospf
     ```

```plaintext
---

Copyright © TOKY Nandrasana
Étudiant de l'École Nationale de l'Informatique
Date : 16 août 2024
```