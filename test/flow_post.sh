#!/bin/bash

# script to be started by flow_setup.sh which runs sr_post in the background.

#adding libcshim posting as well.
export SR_POST_CONFIG='shim_f63.conf'
# The directory we run the flow test scripts in...
tstdir="`pwd`"

httpdocroot=`cat $tstdir/.httpdocroot`

if [ ! -d ${httpdocroot} ]; then
   exit
fi

if [ ! -d ${httpdocroot}/posted_by_shim ]; then
   mkdir  ${httpdocroot}/posted_by_shim
fi


# sr_post initial start
srpostdir=`cat $tstdir/.httpdocroot`/sent_by_tsource2send
srpostlstfile=$httpdocroot/srpostlstfile
srpostlstfile_new=$httpdocroot/srpostlstfile.new
srpostlstfile_old=$httpdocroot/srpostlstfile.old

echo > ${srpostlstfile_old}
# sr_post call

function do_sr_post {

   cd $srpostdir

   # sr_post testing START
   # TODO - consider if .httpdocroot ends with a '/' ?
   find . -type f -print | grep -v '.tmp$'  > $srpostlstfile
   find . -type l -print | grep -v '.tmp$' >> $srpostlstfile
   cat $srpostlstfile    | sort > $srpostlstfile_new

   # Obtain file listing delta

   rm    /tmp/diffs.txt 2> /dev/null
   touch /tmp/diffs.txt
   comm -23 $srpostlstfile_new $srpostlstfile_old > /tmp/diffs.txt

   srpostdelta=`cat /tmp/diffs.txt`

   if [ "$srpostdelta" == "" ]; then
      return
   fi

   # loop on each line to properly post filename with space *** makes too much load on CPU ***

   # cant seem to have success to have .S P C files in /tmp/diffs.txt and have them as correct arguments
   # theses commands would not succeed :
   #cat /tmp/diffs.txt | sed 's/\(.*S P C\)/"\1"/' | sed 's/S P C/S\\ P\\ C/' > /tmp/diffs2.txt
   #cat /tmp/diffs.txt | sed "s/\(.*S P C\)/'\1'/" > /tmp/diffs2.txt
   #cat /tmp/diffs.txt | sed "s/\(.*S P C\)/'\1'/" | sed 's/S P C/S\\ P\\ C/' > /tmp/diffs2.txt

   sr_post -c test2_f61.conf -p `cat /tmp/diffs.txt`
   LD_PRELOAD="libsrshim.so.1" cp -p --parents `cat /tmp/diffs.txt`  ${httpdocroot}/posted_by_shim 
   
   cp -p $srpostlstfile_new $srpostlstfile_old

   do_sr_post

}

# sr_post initial end

while true; do
   sleep 1
   do_sr_post
done

