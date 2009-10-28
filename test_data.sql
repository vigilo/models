--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;


--
-- Name: state_idstat_seq; Type: SEQUENCE SET; Schema: public; Owner: vigiboard
--

SELECT pg_catalog.setval('state_idstate_seq', 47, true);


--
-- Data for Name: graph; Type: TABLE DATA; Schema: public; Owner: vigiboard
--



--
-- Data for Name: graphgroups; Type: TABLE DATA; Schema: public; Owner: vigiboard
--



--
-- Data for Name: graphtogroups; Type: TABLE DATA; Schema: public; Owner: vigiboard
--


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

INSERT INTO service (name, servicetype, command) VALUES ('Charge 01', '1', 'cmd1');
INSERT INTO service (name, servicetype, command) VALUES ('Charge 05', '2', 'cmd2');
INSERT INTO service (name, servicetype, command) VALUES ('Charge 15', '3', 'cmd3');
INSERT INTO service (name, servicetype, command) VALUES ('Collector', '4', 'cmd4');
INSERT INTO service (name, servicetype, command) VALUES ('CPU', '5', 'cmd5');
INSERT INTO service (name, servicetype, command) VALUES ('Entrees / Sorties', '6', 'cmd6');
INSERT INTO service (name, servicetype, command) VALUES ('FakeSNMPVal', '7', 'cmd7');
INSERT INTO service (name, servicetype, command) VALUES ('FakeSNMPVal2', '8', 'cmd8');
INSERT INTO service (name, servicetype, command) VALUES ('Partition Donnees', '9', 'cmd9');
INSERT INTO service (name, servicetype, command) VALUES ('Partition Fausse part', '10', 'cmd10');
INSERT INTO service (name, servicetype, command) VALUES ('Partition Root', '11', 'cmd11');
INSERT INTO service (name, servicetype, command) VALUES ('Processes', '12', 'cmd12');
INSERT INTO service (name, servicetype, command) VALUES ('Processus: cleanup', '13', 'cmd13');
INSERT INTO service (name, servicetype, command) VALUES ('Processus: pop3d', '14', 'cmd14');
INSERT INTO service (name, servicetype, command) VALUES ('Synchro NTP', '15', 'cmd15');
INSERT INTO service (name, servicetype, command) VALUES ('TCP connections', '16', 'cmd16');
INSERT INTO service (name, servicetype, command) VALUES ('Temperature mb_p0_t_core', '17', 'cmd17');
INSERT INTO service (name, servicetype, command) VALUES ('UpTime', '18', 'cmd18');
INSERT INTO service (name, servicetype, command) VALUES ('Ventilateur mb_p0_f0_rs', '19', 'cmd19');
INSERT INTO service (name, servicetype, command) VALUES ('Load', '20', 'cmd19');
INSERT INTO service (name, servicetype, command) VALUES ('HTTPD', '21', 'cmd19');
INSERT INTO service (name, servicetype, command) VALUES ('Interface eth0', '22', 'cmd19');
INSERT INTO service (name, servicetype, command) VALUES ('Interface eth1', '23', 'cmd19');
INSERT INTO service (name, servicetype, command) VALUES ('Interface eth2', '24', 'cmd19');

--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO "group" (name, parent) VALUES ('bla1', NULL);
INSERT INTO "group" (name, parent) VALUES ('bla2', 'bla1');



--
-- Data for Name: grouppermissions; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO grouppermissions (groupname, idpermission) VALUES ('bla1', 2);
INSERT INTO grouppermissions (groupname, idpermission) VALUES ('bla2', 1);


--
-- Data for Name: hostgroups; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO hostgroup (hostname, groupname) VALUES ('ajc.fw.1', 'bla1');
INSERT INTO hostgroup (hostname, groupname) VALUES ('ajc.linux1', 'bla1');
INSERT INTO hostgroup (hostname, groupname) VALUES ('ajc.sw.1', 'bla1');
INSERT INTO hostgroup (hostname, groupname) VALUES ('bdx.fw.1', 'bla1');
INSERT INTO hostgroup (hostname, groupname) VALUES ('bdx.linux1', 'bla1');
INSERT INTO hostgroup (hostname, groupname) VALUES ('brouteur', 'bla1');
INSERT INTO hostgroup (hostname, groupname) VALUES ('bst.fw.1', 'bla1');
INSERT INTO hostgroup (hostname, groupname) VALUES ('bst.unix0', 'bla1');
INSERT INTO hostgroup (hostname, groupname) VALUES ('bst.unix1', 'bla1');
INSERT INTO hostgroup (hostname, groupname) VALUES ('bst.win0', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('messagerie', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('par.fw.1', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('par.linux0', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('par.linux1', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('par.unix0', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('proto4', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('server.mails', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('testaix', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('testnortel', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('testsolaris', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('host1.example.com', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('host2.example.com', 'bla2');
INSERT INTO hostgroup (hostname, groupname) VALUES ('host3.example.com', 'bla2');


--
-- Data for Name: perfdatasource; Type: TABLE DATA; Schema: public; Owner: vigiboard
--





--
-- Data for Name: servicegroups; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO servicegroup (servicename, groupname) VALUES ('Charge 01', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Charge 05', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Charge 15', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Collector', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('CPU', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Entrees / Sorties', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('FakeSNMPVal', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('FakeSNMPVal2', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Partition Donnees', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Partition Fausse part', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Partition Root', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Processes', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Processus: cleanup', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Processus: pop3d', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Synchro NTP', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('TCP connections', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Temperature mb_p0_t_core', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('UpTime', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Ventilateur mb_p0_f0_rs', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Load', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('HTTPD', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Interface eth0', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Interface eth1', 'bla1');
INSERT INTO servicegroup (servicename, groupname) VALUES ('Interface eth2', 'bla1');

--
-- Data for Name: state; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (36, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 'WARNING', 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (37, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 'WARNING', 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (38, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 'WARNING', 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (39, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 'WARNING', 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (41, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 'WARNING', 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (42, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 'WARNING', 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (43, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 'WARNING', 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (44, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 'WARNING', 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (45, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 'WARNING', 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (46, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 'WARNING', 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (47, 'ajc.fw.1', 'Processes', '192.168.1.1', '2009-04-07 13:33:26', 'WARNING', 'SOFT', 2, 'WARNING: Charge 01 average is above 4 (4.5)');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (48, 'host1.example.com', 'Load', '192.168.0.21', '2009-04-07 13:33:26', 'OK', 'SOFT', 2, 'Load is OK');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (49, 'host1.example.com', 'HTTPD', '192.168.0.21', '2009-04-07 13:33:26', 'OK', 'SOFT', 2, 'Appache is OK');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (50, 'host1.example.com', 'Interface eth0', '192.168.0.21', '2009-04-07 13:33:26', 'OK', 'SOFT', 2, 'eth0 is up');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (51, 'host2.example.com', 'Interface eth1', '192.168.0.21', '2009-04-07 13:33:26', 'OK', 'SOFT', 2, 'eth0 is up');
INSERT INTO state (idstate, hostname, servicename, ip, "timestamp", statename, statetype, attempt, message) VALUES (52, 'host3.example.com', 'Interface eth1', '192.168.0.21', '2009-04-07 13:33:26', 'OK', 'SOFT', 2, 'eth0 is up');


--
-- Data for Name: serviceweight; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host1.example.com','Load', 1, 1);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host1.example.com','HTTPD', 1, 1);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host1.example.com','Interface eth0', 1, 1);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host2.example.com','Interface eth1', 1, 1);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host2.example.com','Interface eth2', 1, 1);
INSERT INTO hostservicedata(hostname, servicename, weight, priority) VALUES ('host3.example.com','Interface eth1', 1, 1);



--
--
-- Data for Name: version; Type: TABLE DATA; Schema: public; Owner: vigiboard
--


INSERT INTO version (name, version) VALUES ('vigiboard', '0.1');




--
-- PostgreSQL database dump complete
--

