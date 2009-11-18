--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;


SELECT pg_catalog.setval('state_idstate_seq', 52, true);
SELECT pg_catalog.setval('service_idservice_seq', 26, true);
SELECT pg_catalog.setval('statename_idstatename_seq', 7, true);


--
-- Data for Name: host; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('ajc.fw.1', 'check1', 'com1', 'fqhn1', 'tpl1', '192.168.0.1', 1, 1, '1');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('ajc.linux1', 'check2', 'com2', 'fqhn2', 'tpl2', '192.168.0.2', 2, 2, '2');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('ajc.sw.1', 'check3', 'com3', 'fqhn3', 'tpl3', '192.168.0.3', 3, 3, '3');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('bdx.fw.1', 'check4', 'com4', 'fqhn4', 'tpl4', '192.168.0.4', 4, 4, '4');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('bdx.linux1', 'check5', 'com5', 'fqhn5', 'tpl5', '192.168.0.5', 5, 5, '5');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('brouteur', 'check6', 'com6', 'fqhn6', 'tpl6', '192.168.0.6', 6, 6, '6');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('bst.fw.1', 'check7', 'com7', 'fqhn7', 'tpl7', '192.168.0.7', 7, 7, '7');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('bst.unix0', 'check8', 'com8', 'fqhn8', 'tpl8', '192.168.0.8', 8, 8, '8');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('bst.unix1', 'check9', 'com9', 'fqhn9', 'tpl9', '192.168.0.9', 9, 9, '9');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('bst.win0', 'check10', 'com10', 'fqhn10', 'tpl10', '192.168.0.10', 10, 10, '10');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('messagerie', 'check11', 'com11', 'fqhn11', 'tpl11', '192.168.0.11', 11, 11, '11');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('par.fw.1', 'check12', 'com12', 'fqhn12', 'tpl12', '192.168.0.12', 12, 12, '12');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('par.linux0', 'check13', 'com13', 'fqhn13', 'tpl13', '192.168.0.13', 13, 13, '13');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('par.linux1', 'check14', 'com14', 'fqhn14', 'tpl14', '192.168.0.14', 14, 14, '14');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('par.unix0', 'check15', 'com15', 'fqhn15', 'tpl15', '192.168.0.15', 15, 15, '15');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('proto4', 'check16', 'com16', 'fqhn16', 'tpl16', '192.168.0.16', 16, 16, '16');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('server.mails', 'check17', 'com17', 'fqhn17', 'tpl17', '192.168.0.17', 17, 17, '17');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('testaix', 'check18', 'com18', 'fqhn18', 'tpl18', '192.168.0.18', 18, 18, '18');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('testnortel', 'check19', 'com19', 'fqhn19', 'tpl19', '192.168.0.19', 19, 19, '19');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('testsolaris', 'check20', 'com20', 'fqhn20', 'tpl20', '192.168.0.20', 20, 20, '20');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('host1.example.com', 'check21', 'com21', 'fqhn21', 'tpl21', '192.168.0.21', 21, 21,'21');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('host2.example.com', 'check22', 'com22', 'fqhn22', 'tpl22', '192.168.0.22', 22, 22,'22');
INSERT INTO host (name, checkhostcmd, snmpcommunity, fqhn, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('host3.example.com', 'check23', 'com23', 'fqhn23', 'tpl23', '192.168.0.23', 23, 23,'23');
--
-- Data for Name: service; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (1, 'Charge 01',                  '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (2, 'Charge 05',                  '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (3, 'Charge 15',                  '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (4, 'Collector',                  '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (5, 'CPU',                        '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (6, 'Entrees / Sorties',          '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (7, 'FakeSNMPVal',                '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (8, 'FakeSNMPVal2',               '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (9, 'Partition Donnees',          '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (10, 'Partition Fausse part',     '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (11, 'Partition Root',            '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (12, 'Processes',                 '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (13, 'Processus: cleanup',        '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (14, 'Processus: pop3d',          '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (15, 'Synchro NTP',               '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (16, 'TCP connections',           '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (17, 'Temperature mb_p0_t_core',  '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (18, 'UpTime',                    '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (19, 'Ventilateur mb_p0_f0_rs',   '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (20, 'Load',                      '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (21, 'HTTPD',                     '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (22, 'Interface eth0',            '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (23, 'Interface eth1',            '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (24, 'Interface eth2',            '&', 'lowlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (25, 'Connexion',                 '+', 'highlevel');
INSERT INTO service (idservice, name, op_dep, servicetype) VALUES (26, 'Portail web',               '&', 'highlevel');

INSERT INTO servicelowlevel (idservice, command) VALUES (1, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (2, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (3, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (4, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (5, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (6, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (7, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (8, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (9, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (10, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (11, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (12, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (13, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (14, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (15, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (16, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (17, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (18, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (19, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (20, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (21, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (22, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (23, 'halt');
INSERT INTO servicelowlevel (idservice, command) VALUES (24, 'halt');

INSERT INTO servicehighlevel (idservice, message, warning_threshold, critical_threshold, weight) VALUES (25, 'Ouch', 300, 150, NULL);
INSERT INTO servicehighlevel (idservice, message, warning_threshold, critical_threshold, weight) VALUES (26, 'Ouch', 300, 150, NULL);

INSERT INTO servicedephigh (iddep, servicename, type_dep) VALUES (1, 'Connexion', 'lowlevel');
INSERT INTO servicedephighonlow (iddep, host_dep, service_dep) VALUES(1, 'host2.example.com', 'Interface eth0');
INSERT INTO servicedephigh (iddep, servicename, type_dep) VALUES (2, 'Connexion', 'lowlevel');
INSERT INTO servicedephighonlow (iddep, host_dep, service_dep) VALUES(2, 'host2.example.com', 'Interface eth1');
INSERT INTO servicedephigh (iddep, servicename, type_dep) VALUES (3, 'Connexion', 'lowlevel');
INSERT INTO servicedephighonlow (iddep, host_dep, service_dep) VALUES(3, 'host2.example.com', 'Interface eth2');

INSERT INTO servicedephigh (iddep, servicename, type_dep) VALUES (4, 'Portail web', 'lowlevel');
INSERT INTO servicedephighonlow (iddep, host_dep, service_dep) VALUES(4, 'host2.example.com', 'HTTPD');
INSERT INTO servicedephigh (iddep, servicename, type_dep) VALUES (5, 'Portail web', 'highlevel');
INSERT INTO servicedephighonhigh (iddep, service_dep) VALUES(5, 'Connexion');

--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO "group" (name, idparent) VALUES ('Serveurs', NULL);
INSERT INTO "group" (name, idparent) VALUES ('Serveurs Linux', 1);
INSERT INTO "group" (name, idparent) VALUES ('Serveurs Windows', 1);



--
-- Data for Name: grouppermissions; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO grouppermissions (idgroup, idpermission) VALUES (1, 2);
INSERT INTO grouppermissions (idgroup, idpermission) VALUES (2, 1);


--
-- Data for Name: hostgroups; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO hostgroup (hostname, idgroup) VALUES ('ajc.fw.1', 1);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('ajc.linux1', 1);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('ajc.sw.1', 1);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('bdx.fw.1', 1);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('bdx.linux1', 1);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('brouteur', 1);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('bst.fw.1', 1);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('bst.unix0', 1);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('bst.unix1', 1);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('bst.win0', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('messagerie', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('par.fw.1', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('par.linux0', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('par.linux1', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('par.unix0', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('proto4', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('server.mails', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('testaix', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('testnortel', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('testsolaris', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('host1.example.com', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('host2.example.com', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('host3.example.com', 2);


--
-- Data for Name: perfdatasource; Type: TABLE DATA; Schema: public; Owner: vigiboard
--





--
-- Data for Name: servicegroups; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO servicegroup (servicename, idgroup) VALUES ('Charge 01', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Charge 05', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Charge 15', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Collector', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('CPU', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Entrees / Sorties', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('FakeSNMPVal', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('FakeSNMPVal2', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Partition Donnees', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Partition Fausse part', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Partition Root', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Processes', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Processus: cleanup', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Processus: pop3d', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Synchro NTP', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('TCP connections', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Temperature mb_p0_t_core', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('UpTime', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Ventilateur mb_p0_f0_rs', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Load', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('HTTPD', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Interface eth0', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Interface eth1', 1);
INSERT INTO servicegroup (servicename, idgroup) VALUES ('Interface eth2', 1);

--
-- Data for Name: statename; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO statename (idstatename, statename, "order") VALUES (1, 'OK', 0);
INSERT INTO statename (idstatename, statename, "order") VALUES (2, 'UNKNOWN', 1);
INSERT INTO statename (idstatename, statename, "order") VALUES (3, 'WARNING', 2);
INSERT INTO statename (idstatename, statename, "order") VALUES (4, 'CRITICAL', 3);
INSERT INTO statename (idstatename, statename, "order") VALUES (5, 'UP', 0);
INSERT INTO statename (idstatename, statename, "order") VALUES (7, 'UNREACHABLE', 1);
INSERT INTO statename (idstatename, statename, "order") VALUES (6, 'DOWN', 3);

--
-- Data for Name: state; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (36, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 3, 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (37, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 3, 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (38, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 3, 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (39, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 3, 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (41, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 3, 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (42, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 3, 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (43, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 3, 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (44, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 3, 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (45, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 3, 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (46, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 3, 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (47, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 3, 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (48, 'host1.example.com', 'Load', '192.168.0.21', '2009-04-07 13:33:26', 1, 'SOFT', 2, 'Load is OK');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (49, 'host1.example.com', 'HTTPD', '192.168.0.21', '2009-04-07 13:33:26', 1, 'SOFT', 2, 'Apache is OK');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (50, 'host1.example.com', 'Interface eth0', '192.168.0.21', '2009-04-07 13:33:26', 1, 'SOFT', 2, 'eth0 is up');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (51, 'host2.example.com', 'Interface eth1', '192.168.0.21', '2009-04-07 13:33:26', 1, 'SOFT', 2, 'eth1 is up');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", state, statetype, attempt, message) VALUES (52, 'host3.example.com', 'Interface eth1', '192.168.0.21', '2009-04-07 13:33:26', 1, 'SOFT', 2, 'eth2 is up');


--
-- Data for Name: serviceweight; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host1.example.com','Load', 1, 1);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host1.example.com','HTTPD', 1, 1);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host1.example.com','Interface eth0', 1, 1);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host2.example.com','Interface eth0', 100, 4);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host2.example.com','Interface eth1', 120, 4);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host2.example.com','Interface eth2', 130, 4);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host2.example.com','HTTPD', 200, 1);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host3.example.com','Interface eth1', 1, 4);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('proto4', 'Processes', 100, 2);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('proto4', 'UpTime', 100, 2);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('proto4', 'CPU', 100, 2);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('brouteur', 'Processes', 100, 3);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('brouteur', 'UpTime', 100, 2);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('brouteur', 'CPU', 100, 1);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('messagerie', 'Processes', 100, 1);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('messagerie', 'UpTime', 100, 2);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('messagerie', 'CPU', 100, 3);


--
--
-- Data for Name: version; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

-- On va plutut stocker un numero de version pour le modele dans la table,
-- au lieu d'un numero de version par application.
-- INSERT INTO version (name, version) VALUES ('vigiboard', '0.1');




--
-- PostgreSQL database dump complete
--
