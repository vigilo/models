#!/bin/bash
# lié à 038_HLS_refactoring
# Copyright (C) 2014-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

BDD="vigilo"



NBR=`echo "SELECT count(*) FROM vigilo_highlevelservice;" | su - postgres -c "psql -d $BDD -Anqt"`
inc=0
echo '<?xml version="1.0"?>

<hlservices>'

echo -n "SELECT * FROM vigilo_highlevelservice ORDER BY servicename;" | su - postgres -c "psql -d $BDD -Anqt" | \
while read line; do
    inc=$(($inc+1))
    echo -ne "\r$inc/$NBR" >&2
    # idservice | servicename |                        message                        | warning_threshold | critical_threshold | weight | warning_weight
    #-----------+-------------+-------------------------------------------------------+-------------------+--------------------+--------+----------------
    idservice=`         echo $line | awk -F "|" '{ print $1 }'`
    servicename=`       echo $line | awk -F "|" '{ print $2 }'`
    message=`           echo $line | awk -F "|" '{ print $3 }'`
    warning_threshold=` echo $line | awk -F "|" '{ print $4 }'`
    critical_threshold=`echo $line | awk -F "|" '{ print $5 }'`
    weight=`            echo $line | awk -F "|" '{ print $6 }'`
    warning_weight=`    echo $line | awk -F "|" '{ print $7 }'`

    unknown_priority=` echo "SELECT priority FROM vigilo_hlspriority WHERE idhls=${idservice} AND idstatename=2;" | su - postgres -c "psql -d $BDD -Anqt"`
    warning_priority=` echo "SELECT priority FROM vigilo_hlspriority WHERE idhls=${idservice} AND idstatename=3;" | su - postgres -c "psql -d $BDD -Anqt"`
    critical_priority=`echo "SELECT priority FROM vigilo_hlspriority WHERE idhls=${idservice} AND idstatename=4;" | su - postgres -c "psql -d $BDD -Anqt"`

    operator=`echo "SELECT operator FROM vigilo_dependencygroup WHERE iddependent=${idservice};" | su - postgres -c "psql -d $BDD -Anqt"`
    case $operator in
        "&") operator="AND" ;;
        "|") operator="OR" ;;
        "+") operator="PLUS" ;;
          *) echo "ERROR: operator unknown $operator" >&2 ; exit 1 ;;
    esac

    echo ""
    echo "<hlservice name=\"$servicename\">

    <message>$message</message>

    <warning_threshold>$warning_threshold</warning_threshold>
    <critical_threshold>$critical_threshold</critical_threshold>

    <unknown_priority>$unknown_priority</unknown_priority>
    <warning_priority>$warning_priority</warning_priority>
    <critical_priority>$critical_priority</critical_priority>

    <operator>$operator</operator>
"
    # pour les HLS

    echo "SELECT hls.servicename, d.weight, d.warning_weight
              FROM vigilo_dependencygroup dg
              JOIN vigilo_dependency d ON d.idgroup = dg.idgroup
              JOIN vigilo_highlevelservice hls ON hls.idservice = d.idsupitem
              WHERE dg.iddependent=${idservice}
              ORDER BY hls.servicename ASC;" | su - postgres -c "psql -d $BDD -Anqt" | \
    while read l_hls; do
        dhlsservicename=`   echo $l_hls | awk -F "|" '{ print $1 }'`
        dhlsweight=`        echo $l_hls | awk -F "|" '{ print $2 }'`
        dhlswarning_weight=`echo $l_hls | awk -F "|" '{ print $3 }'`

        if [ "$dhlswarning_weight" == "$dhlsweight" ] ; then
            dhlswarning_weight=""
        else
            dhlswarning_weight=" warning_weight=\"$dhlswarning_weight\""
        fi
        if [ $dhlsweight == "1" ] ; then
            dhlsweight=""
        else
            dhlsweight=" weight=\"$dhlsweight\""
        fi
        echo "    <depends service=\"$dhlsservicename\"${dhlsweight}${dhlswarning_weight}/>"
    done


    # pour les hôtes

    echo "SELECT h.name, d.weight
              FROM vigilo_dependencygroup dg
              JOIN vigilo_dependency d ON d.idgroup = dg.idgroup
              JOIN vigilo_host h ON h.idhost = d.idsupitem
              WHERE dg.iddependent=${idservice}
              ORDER BY h.name ASC;" | su - postgres -c "psql -d $BDD -Anqt" | \
    while read l_h; do
        dhname=`  echo $l_h | awk -F "|" '{ print $1 }'`
        dhweight=`echo $l_h | awk -F "|" '{ print $2 }'`

        if [ -n "$dhweight" ] ; then
            if [ $dhweight == "1" ] ; then
                dhsweight=""
            else
                dhweight=" weight=\"$dhweight\""
            fi
        fi
        echo "    <depends host=\"$dhname\"${dhweight}/>"
    done


    # pour les services
    echo "SELECT h.name, lls.servicename, d.weight, d.warning_weight
              FROM vigilo_dependencygroup dg
              JOIN vigilo_dependency d ON d.idgroup = dg.idgroup
              JOIN vigilo_lowlevelservice lls ON lls.idservice = d.idsupitem
              JOIN vigilo_host h ON h.idhost = lls.idhost
              WHERE dg.iddependent=${idservice}
              ORDER BY h.name ASC, lls.servicename ASC;" | su - postgres -c "psql -d $BDD -Anqt" | \
    while read l_lls; do
        dhname=`            echo $l_lls | awk -F "|" '{ print $1 }'`
        dservicename=`      echo $l_lls | awk -F "|" '{ print $2 }'`
        dllsweight=`        echo $l_lls | awk -F "|" '{ print $3 }'`
        dllswarning_weight=`echo $l_lls | awk -F "|" '{ print $4 }'`

        if [ "$dllswarning_weight" == "$dllsweight" ] ; then
            dllswarning_weight=""
        else
            dllswarning_weight=" warning_weight=\"$dllswarning_weight\""
        fi
        if [ "$dllsweight" == "1" ] ; then
            dllsweight=""
        else
            dllsweight=" weight=\"$dllsweight\""
        fi
        echo "    <depends host=\"$dhname\" service=\"$dservicename\"${dllsweight}${dllswarning_weight}/>"
    done
    echo "</hlservice>"
done

echo '</hlservices>'


echo -e "\r$NBR/$NBR" >&2
