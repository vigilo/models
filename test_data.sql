--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;


SELECT pg_catalog.setval('correvent_idcorrevent_seq', 1, false);
SELECT pg_catalog.setval('event_idevent_seq', 1, false);
SELECT pg_catalog.setval('eventhistory_idhistory_seq', 1, false);
SELECT pg_catalog.setval('group_idgroup_seq', 1, false);
SELECT pg_catalog.setval('hostclass_idclass_seq', 1, false);
SELECT pg_catalog.setval('map_idmap_seq', 1, false);
SELECT pg_catalog.setval('maplink_idmaplink_seq', 1, false);
SELECT pg_catalog.setval('mapnode_idmapnode_seq', 1, false);
SELECT pg_catalog.setval('statename_idstatename_seq', 1, false);
SELECT pg_catalog.setval('supitem_idsupitem_seq', 1, false);
SELECT pg_catalog.setval('vigiloserver_idsrv_seq', 1, false);


--
-- Data for Name: supitem; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

-- Services de bas niveau.
INSERT INTO supitem (idsupitem, itemtype) VALUES (1, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (2, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (3, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (4, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (5, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (6, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (7, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (8, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (9, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (10, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (11, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (12, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (13, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (14, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (15, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (16, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (17, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (18, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (19, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (20, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (21, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (22, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (23, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (24, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (25, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (26, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (27, 'lowlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (28, 'lowlevel');

-- Services de haut niveau
INSERT INTO supitem (idsupitem, itemtype) VALUES (29, 'highlevel');
INSERT INTO supitem (idsupitem, itemtype) VALUES (30, 'highlevel');

-- Hotes.
INSERT INTO supitem (idsupitem, itemtype) VALUES (31, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (32, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (33, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (34, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (35, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (36, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (37, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (38, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (39, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (40, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (41, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (42, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (43, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (44, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (45, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (46, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (47, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (48, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (49, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (50, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (51, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (52, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (53, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (54, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (55, 'host');
INSERT INTO supitem (idsupitem, itemtype) VALUES (56, 'host');

--
-- Data for Name: host; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 31, 'ajc.fw.1', 'check1', 'com1', 'tpl1', '192.168.0.1', 1, 1, '1');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 32, 'ajc.linux1', 'check2', 'com2',   'tpl2', '192.168.0.2', 2, 2, '2');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 33, 'ajc.sw.1', 'check3', 'com3', 'tpl3', '192.168.0.3', 3, 3, '3');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 34, 'bdx.fw.1', 'check4', 'com4', 'tpl4', '192.168.0.4', 4, 4, '4');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 35, 'bdx.linux1', 'check5', 'com5', 'tpl5', '192.168.0.5', 5, 5, '5');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 36, 'brouteur', 'check6', 'com6', 'tpl6', '192.168.0.6', 6, 6, '6');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 37, 'bst.fw.1', 'check7', 'com7', 'tpl7', '192.168.0.7', 7, 7, '7');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 38, 'bst.unix0', 'check8', 'com8', 'tpl8', '192.168.0.8', 8, 8, '8');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 39, 'bst.unix1', 'check9', 'com9', 'tpl9', '192.168.0.9', 9, 9, '9');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 40, 'bst.win0', 'check10', 'com10', 'tpl10', '192.168.0.10', 10, 10, '10');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 41, 'messagerie', 'check11', 'com11', 'tpl11', '192.168.0.11', 11, 11, '11');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 42, 'par.fw.1', 'check12', 'com12', 'tpl12', '192.168.0.12', 12, 12, '12');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 43, 'par.linux0', 'check13', 'com13', 'tpl13', '192.168.0.13', 13, 13, '13');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 44, 'par.linux1', 'check14', 'com14', 'tpl14', '192.168.0.14', 14, 14, '14');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 45, 'par.unix0', 'check15', 'com15', 'tpl15', '192.168.0.15', 15, 15, '15');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 46, 'proto4', 'check16', 'com16', 'tpl16', '192.168.0.16', 16, 16, '16');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 47, 'server.mails', 'check17', 'com17', 'tpl17', '192.168.0.17', 17, 17, '17');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 48, 'testaix', 'check18', 'com18', 'tpl18', '192.168.0.18', 18, 18, '18');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 49, 'testnortel', 'check19', 'com19', 'tpl19', '192.168.0.19', 19, 19, '19');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 50, 'testsolaris', 'check20', 'com20', 'tpl20', '192.168.0.20', 20, 20, '20');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 51, 'host1.example.com', 'check21', 'com21', 'tpl21', '192.168.0.21', 21, 21,'21');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 52, 'host2.example.com', 'check22', 'com22', 'tpl22', '192.168.0.22', 22, 22,'22');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 53, 'host3.example.com', 'check23', 'com23', 'tpl23', '192.168.0.23', 23, 23,'23');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 54, 'routeur1', 'check24', 'com24', 'tpl24', '192.168.0.24', 24, 24,'24');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 55, 'routeur2', 'check25', 'com25', 'tpl25', '192.168.0.25', 25, 25,'25');
INSERT INTO host (weight, idhost, name, checkhostcmd, snmpcommunity, hosttpl, mainip, snmpport, snmpoidsperpdu, snmpversion)
    VALUES (42, 56, 'firewall', 'check26', 'com26', 'tpl26', '192.168.0.26', 26, 26,'26');


--
-- Data for Name: service; Type: TABLE DATA; Schema: public; Owner: vigiboard
--

INSERT INTO service (idservice, servicename, op_dep) VALUES (1, 'Interface eth0',          '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (2, 'Interface eth0',          '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (3, 'Interface eth0',          '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (4, 'Interface eth0',          '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (5, 'Interface eth0',          '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (6, 'Interface eth0',          '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (7, 'Interface eth1',          '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (8, 'Interface eth1',          '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (9, 'Interface eth1',          '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (10, 'Interface eth1',         '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (11, 'Interface eth1',         '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (12, 'Interface eth2',         '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (13, 'UpTime',                 '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (14, 'UpTime',                 '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (15, 'UpTime',                 '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (16, 'CPU',                    '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (17, 'CPU',                    '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (18, 'CPU',                    '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (19, 'CPU',                    '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (20, 'Load',                   '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (21, 'Processes',              '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (22, 'Processes',              '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (23, 'Processes',              '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (24, 'Processes',              '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (25, 'HTTPD',                  '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (26, 'HTTPD',                  '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (27, 'RAM',                    '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (28, 'RAM',                    '&');
INSERT INTO service (idservice, servicename, op_dep) VALUES (29, 'Connexion',              '+');
INSERT INTO service (idservice, servicename, op_dep) VALUES (30, 'Portail web',            '&');

INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (1, 51, 'halt', 1, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (2, 52, 'halt', 100, 4);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (3, 41, 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (4, 56, 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (5, 55, 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (6, 54, 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (7, 52, 'halt', 120, 4);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (8, 53, 'halt', 1, 4);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (9, 56, 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (10, 54, 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (11, 55, 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (12, 52, 'halt', 130, 4);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (13, 46, 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (14, 36, 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (15, 41, 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (16, 46, 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (17, 36, 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (18, 41, 'halt', 100, 3);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (19, 51, 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (20, 51, 'halt', 1, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (21, 46, 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (22, 36, 'halt', 100, 3);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (23, 41, 'halt', 100, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (24, 51, 'halt', 100, 2);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (25, 51, 'halt', 1, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (26, 52, 'halt', 200, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (27, 41, 'halt', 1, 1);
INSERT INTO servicelowlevel(idservice, idhost, command, weight, priority) VALUES (28, 51, 'halt', 200, 1);

INSERT INTO servicehighlevel (idservice, message, warning_threshold, critical_threshold, weight) VALUES (29, 'Ouch', 300, 150, NULL);
INSERT INTO servicehighlevel (idservice, message, warning_threshold, critical_threshold, weight) VALUES (30, 'Ouch', 300, 150, NULL);


INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (29, 2);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (29, 7);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (29, 12);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (30, 26);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (30, 29);

INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (23, 18);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (23, 27);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (18, 3);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (27, 3);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (3, 10);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (3, 11);

INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (24, 19);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (24, 28);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (19, 1);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (28, 1);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (1, 9);

INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (9, 4);

INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (4, 10);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (4, 11);

INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (10, 6);
INSERT INTO dependency (idsupitem1, idsupitem2) VALUES (11, 5);


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

INSERT INTO hostgroup (idhost, idgroup) VALUES (31, 1);
INSERT INTO hostgroup (idhost, idgroup) VALUES (32, 1);
INSERT INTO hostgroup (idhost, idgroup) VALUES (33, 1);
INSERT INTO hostgroup (idhost, idgroup) VALUES (34, 1);
INSERT INTO hostgroup (idhost, idgroup) VALUES (35, 1);
INSERT INTO hostgroup (idhost, idgroup) VALUES (36, 1);
INSERT INTO hostgroup (idhost, idgroup) VALUES (37, 1);
INSERT INTO hostgroup (idhost, idgroup) VALUES (38, 1);
INSERT INTO hostgroup (idhost, idgroup) VALUES (39, 1);
INSERT INTO hostgroup (idhost, idgroup) VALUES (40, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (41, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (42, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (43, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (44, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (45, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (46, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (47, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (48, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (49, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (50, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (51, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (52, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (53, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (54, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (55, 2);
INSERT INTO hostgroup (idhost, idgroup) VALUES (56, 2);


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

