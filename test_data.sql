--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;


SELECT pg_catalog.setval('event_idevent_seq', 1, false);
SELECT pg_catalog.setval('eventhistory_idhistory_seq', 1, false);
SELECT pg_catalog.setval('eventsaggregate_idaggregate_seq', 1, false);
SELECT pg_catalog.setval('group_idgroup_seq', 1, false);
SELECT pg_catalog.setval('hostclass_idclass_seq', 1, false);
SELECT pg_catalog.setval('map_idmap_seq', 1, false);
SELECT pg_catalog.setval('maplink_idmaplink_seq', 1, false);
SELECT pg_catalog.setval('mapnode_idmapnode_seq', 1, false);
SELECT pg_catalog.setval('service_idservice_seq', 1, false);
SELECT pg_catalog.setval('statename_idstatename_seq', 1, false);
SELECT pg_catalog.setval('vigiloserver_idsrv_seq', 1, false);


--
-- Data for Name: host; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('ajc.fw.1', 'check1', 'com1', 'tpl1', '192.168.0.1', 1, 1, '1');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('ajc.linux1', 'check2', 'com2',   'tpl2', '192.168.0.2', 2, 2, '2');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('ajc.sw.1', 'check3', 'com3', 'tpl3', '192.168.0.3', 3, 3, '3');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('bdx.fw.1', 'check4', 'com4', 'tpl4', '192.168.0.4', 4, 4, '4');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('bdx.linux1', 'check5', 'com5', 'tpl5', '192.168.0.5', 5, 5, '5');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('brouteur', 'check6', 'com6', 'tpl6', '192.168.0.6', 6, 6, '6');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('bst.fw.1', 'check7', 'com7', 'tpl7', '192.168.0.7', 7, 7, '7');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('bst.unix0', 'check8', 'com8', 'tpl8', '192.168.0.8', 8, 8, '8');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('bst.unix1', 'check9', 'com9', 'tpl9', '192.168.0.9', 9, 9, '9');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('bst.win0', 'check10', 'com10', 'tpl10', '192.168.0.10', 10, 10, '10');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('messagerie', 'check11', 'com11', 'tpl11', '192.168.0.11', 11, 11, '11');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('par.fw.1', 'check12', 'com12', 'tpl12', '192.168.0.12', 12, 12, '12');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('par.linux0', 'check13', 'com13', 'tpl13', '192.168.0.13', 13, 13, '13');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('par.linux1', 'check14', 'com14', 'tpl14', '192.168.0.14', 14, 14, '14');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('par.unix0', 'check15', 'com15', 'tpl15', '192.168.0.15', 15, 15, '15');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('proto4', 'check16', 'com16', 'tpl16', '192.168.0.16', 16, 16, '16');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('server.mails', 'check17', 'com17', 'tpl17', '192.168.0.17', 17, 17, '17');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('testaix', 'check18', 'com18', 'tpl18', '192.168.0.18', 18, 18, '18');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('testnortel', 'check19', 'com19', 'tpl19', '192.168.0.19', 19, 19, '19');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('testsolaris', 'check20', 'com20', 'tpl20', '192.168.0.20', 20, 20, '20');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('host1.example.com', 'check21', 'com21', 'tpl21', '192.168.0.21', 21, 21,'21');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('host2.example.com', 'check22', 'com22', 'tpl22', '192.168.0.22', 22, 22,'22');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('host3.example.com', 'check23', 'com23', 'tpl23', '192.168.0.23', 23, 23,'23');

INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('routeur1', 'check24', 'com24', 'tpl24', '192.168.0.24', 24, 24,'24');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('routeur2', 'check25', 'com25', 'tpl25', '192.168.0.25', 25, 25,'25');
INSERT INTO host (name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion) VALUES ('firewall', 'check26', 'com26', 'tpl26', '192.168.0.26', 26, 26,'26');


--
-- Data for Name: service; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (1, 'Interface eth0',          '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (2, 'Interface eth0',          '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (3, 'Interface eth0',          '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (4, 'Interface eth0',          '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (5, 'Interface eth0',          '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (6, 'Interface eth0',          '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (7, 'Interface eth1',          '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (8, 'Interface eth1',          '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (9, 'Interface eth1',          '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (10, 'Interface eth1',         '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (11, 'Interface eth1',         '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (12, 'Interface eth2',         '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (13, 'UpTime',                 '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (14, 'UpTime',                 '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (15, 'UpTime',                 '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (16, 'CPU',                    '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (17, 'CPU',                    '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (18, 'CPU',                    '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (19, 'CPU',                    '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (20, 'Load',                   '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (21, 'Processes',              '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (22, 'Processes',              '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (23, 'Processes',              '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (24, 'Processes',              '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (25, 'HTTPD',                  '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (26, 'HTTPD',                  '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (27, 'RAM',                    '&', 'lowlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (28, 'RAM',                    '&', 'lowlevel');

INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (29, 'Connexion',              '+', 'highlevel');
INSERT INTO service (idservice, servicename, op_dep, servicetype) VALUES (30, 'Portail web',            '&', 'highlevel');

INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (1, 'host1.example.com', 'halt', 1, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (2, 'host2.example.com', 'halt', 100, 4);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (3, 'messagerie', 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (4, 'firewall', 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (5, 'routeur2', 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (6, 'routeur1', 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (7, 'host2.example.com', 'halt', 120, 4);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (8, 'host3.example.com', 'halt', 1, 4);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (9, 'firewall', 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (10, 'routeur1', 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (11, 'routeur2', 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (12, 'host2.example.com', 'halt', 130, 4);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (13, 'proto4', 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (14, 'brouteur', 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (15, 'messagerie', 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (16, 'proto4', 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (17, 'brouteur', 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (18, 'messagerie', 'halt', 100, 3);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (19, 'host1.example.com', 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (20, 'host1.example.com', 'halt', 1, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (21, 'proto4', 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (22, 'brouteur', 'halt', 100, 3);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (23, 'messagerie', 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (24, 'host1.example.com', 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (25, 'host1.example.com', 'halt', 1, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (26, 'host2.example.com', 'halt', 200, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (27, 'messagerie', 'halt', 1, 1);
INSERT INTO servicelowlevel(idservice, hostname, command, weight, priority) VALUES (28, 'host1.example.com', 'halt', 200, 1);

INSERT INTO servicehighlevel (idservice, message, warning_threshold, critical_threshold, weight) VALUES (29, 'Ouch', 300, 150, NULL);
INSERT INTO servicehighlevel (idservice, message, warning_threshold, critical_threshold, weight) VALUES (30, 'Ouch', 300, 150, NULL);


INSERT INTO servicedephigh (iddep, idservice, type_dep) VALUES (1, 29, 'lowlevel');
INSERT INTO servicedephighonlow (iddep, iddepservice) VALUES(1, 2);

INSERT INTO servicedephigh (iddep, idservice, type_dep) VALUES (2, 29, 'lowlevel');
INSERT INTO servicedephighonlow (iddep, iddepservice) VALUES(2, 7);

INSERT INTO servicedephigh (iddep, idservice, type_dep) VALUES (3, 29, 'lowlevel');
INSERT INTO servicedephighonlow (iddep, iddepservice) VALUES(3, 12);

INSERT INTO servicedephigh (iddep, idservice, type_dep) VALUES (4, 30, 'lowlevel');
INSERT INTO servicedephighonlow (iddep, iddepservice) VALUES(4, 26);

INSERT INTO servicedephigh (iddep, idservice, type_dep) VALUES (5, 30, 'highlevel');
INSERT INTO servicedephighonhigh (iddep, idservice_dep) VALUES(5, 29);


INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (23, 18);
INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (23, 27);
INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (18, 3);
INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (27, 3);
INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (3, 10);
INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (3, 11);

INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (24, 19);
INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (24, 28);
INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (19, 1);
INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (28, 1);
INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (1, 9);

INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (9, 4);

INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (4, 10);
INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (4, 11);

INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (10, 6);
INSERT INTO servicedeplowonlow (idservice, iddep) VALUES (11, 5);


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO "group" (name, idparent, grouptype) VALUES ('Serveurs', NULL, 'hostgroup');
INSERT INTO "group" (name, idparent, grouptype) VALUES ('Serveurs Linux', 1, 'hostgroup');
INSERT INTO "group" (name, idparent, grouptype) VALUES ('Serveurs Windows', 1, 'hostgroup');


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
INSERT INTO hostgroup (hostname, idgroup) VALUES ('routeur1', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('routeur2', 2);
INSERT INTO hostgroup (hostname, idgroup) VALUES ('firewall', 2);


--
-- Data for Name: perfdatasource; Type: TABLE DATA; Schema: public; Owner: vigiboard
--





--
-- Data for Name: servicegroups; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO servicegroup (idservice, idgroup) VALUES (1, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (2, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (3, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (4, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (5, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (6, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (7, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (8, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (9, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (10, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (11, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (12, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (13, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (14, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (15, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (16, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (17, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (18, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (19, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (20, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (21, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (22, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (23, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (24, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (25, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (26, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (27, 1);
INSERT INTO servicegroup (idservice, idgroup) VALUES (28, 1);

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
--
-- Data for Name: version; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

-- On va plutut stocker un numero de version pour le modele dans la table,
-- au lieu d'un numero de version par application.
-- INSERT INTO version (name, version) VALUES ('vigiboard', '0.1');


--
-- PostgreSQL database dump complete
--

