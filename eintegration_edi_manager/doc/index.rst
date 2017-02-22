EDI Manager Documentation
=========================

Configuration
-------------

EDI Messages
''''''''''''

At first, an EDI message which will be used to send a particular business object needs to be defined in the EDI Messages section.

.. figure:: edi_msg.png
   :align: left


EDI Templates
'''''''''''''

Then an EDI template has to be created. The template name, the EDI message type and the business object type can be set here.

.. figure:: edi_template.png
   :align: left

Next upon clicking the "Select Related Entities" button the relationships dialog appears. This dialog allows to select which relationships from the connected business object will be added into the xml file which will be sent afterwards. The selection process is finished by clicking on the "Confirm" button.

.. figure:: edi_template_rel.png
   :align: left

EDI Document Partners
'''''''''''''''''''''

Every contact in Odoo can have multiple EDI documents partners with different GLNs connected to it. EDI document partners can be selected as recipients of EDI documents.

.. figure:: edi_recipients.png
   :align: left

Sending EDI Documents
---------------------

Single Invoice
''''''''''''''

EDI documents can be created from an invoice by clicking on the "Send by EDI" button. All EDI documents connected to a particular invoice are displayed on the "EDI Documents" tab page at the bottom. Only invoices in the "Open" state are processed.

.. figure:: edi_invoice.png
   :align: left

Multiple Invoices
'''''''''''''''''

There is also a multi action available to create EDI documents from the selected invoices in the "Open" state.

.. figure:: edi_invoice_multi.png
   :align: left

Results Summary
---------------

EDI Document List
'''''''''''''''''

All existing EDI documents can be access under the "EDI" menu. The documents in the "To Be Sent" stage are automatically processed by a cron job but there is also a multi action available to send the documents immediately.

.. figure:: edi_documents.png
   :align: left

Outgoing Email With The EDI Document
''''''''''''''''''''''''''''''''''''

The recipients of EDI documents receive an email with an xml file which contains the data from the source invoice.
