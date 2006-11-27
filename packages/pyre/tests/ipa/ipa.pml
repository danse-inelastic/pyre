<?xml version="1.0"?>
<!--
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!
!                             Michael A.G. Aivazis
!                      California Institute of Technology
!                      (C) 1998-2005  All Rights Reserved
!
! {LicenseText}
!
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-->


<!DOCTYPE inventory>

<inventory>

  <component name='ipa'>

    <property name='port'>50001</property>
    <property name='timeout'>10*second</property>
    <property name='ticketDuration'>20*second</property>

    <component name='userManager'>
      <property name='passwd'>userdb.md5</property>
    </component>
  </component>

</inventory>


<!-- version-->
<!-- $Id: ipa.pml,v 1.1.1.1 2006-11-27 00:10:11 aivazis Exp $-->

<!-- End of file -->
