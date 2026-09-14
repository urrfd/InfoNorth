# Fortnox object notes

One note per API resource: **87 resources**, 405 operations, 
249 paths. Generated from the OpenAPI specification in 
`../openapi.json` — see `../../scripts/generate_object_notes.py`.

Each note carries the resource's endpoints, the collection key needed by
`FortnoxClient.paginate`, its fields, its filters, and the safety rules that apply
to its write operations. Read the note for a resource before calling it.

**The field and filter lists are derived from the spec, not from observed traffic.**
They describe what Fortnox documents, which is not always what a given company
returns. Each note has a `Date tested` line recording whether anyone has checked.

## Company-Order-Bank-Process-API

- [CompanyOrderBankProcess](company-order-bank-process-api-companyorderbankprocess.md) — GET, PATCH, POST, PUT ⚠️ writes
- [StartCompanyOrderBankProcess](company-order-bank-process-api-startcompanyorderbankprocess.md) — GET, PATCH, POST ⚠️ writes

## Company-Order-Bank-Process-Webhook-API

- [BankProcessWebhook](company-order-bank-process-webhook-api-bankprocesswebhook.md) — DELETE, GET, PATCH, POST ⚠️ writes

## Recurring-API

- [InvoiceRequests](recurring-api-invoicerequests.md) — GET, POST ⚠️ writes
- [RecurringDeviations](recurring-api-recurringdeviations.md) — GET
- [Recurrings](recurring-api-recurrings.md) — GET, PATCH, POST, PUT ⚠️ writes

## fileattachments

- [Attachment](fileattachments-attachment.md) — DELETE, GET, POST, PUT ⚠️ writes

## fortnox

- [AbsenceTransactions](fortnox-absencetransactions.md) — DELETE, GET, POST, PUT ⚠️ writes
- [AccountCharts](fortnox-accountcharts.md) — GET
- [Accounts](fortnox-accounts.md) — DELETE, GET, POST, PUT ⚠️ writes
- [Archive](fortnox-archive.md) — DELETE, GET, POST ⚠️ writes
- [ArticleFileConnections](fortnox-articlefileconnections.md) — DELETE, GET, POST ⚠️ writes
- [ArticleUrlConnection](fortnox-articleurlconnection.md) — DELETE, GET, POST, PUT ⚠️ writes
- [ArticleUrlConnections](fortnox-articleurlconnections.md) — GET
- [Articles](fortnox-articles.md) — DELETE, GET, POST, PUT ⚠️ writes
- [AssetFileConnection](fortnox-assetfileconnection.md) — DELETE, GET, POST ⚠️ writes
- [AssetTypes](fortnox-assettypes.md) — DELETE, GET, POST, PUT ⚠️ writes
- [Assets](fortnox-assets.md) — DELETE, GET, POST, PUT ⚠️ writes
- [AttendanceTransactions](fortnox-attendancetransactions.md) — DELETE, GET, POST, PUT ⚠️ writes
- [CompanyInformation](fortnox-companyinformation.md) — GET
- [CompanySettings](fortnox-companysettings.md) — GET
- [ContractAccruals](fortnox-contractaccruals.md) — DELETE, GET, POST, PUT ⚠️ writes
- [ContractTemplates](fortnox-contracttemplates.md) — GET, POST, PUT ⚠️ writes
- [Contracts](fortnox-contracts.md) — GET, POST, PUT ⚠️ writes
- [CostCenters](fortnox-costcenters.md) — DELETE, GET, POST, PUT ⚠️ writes
- [Currencies](fortnox-currencies.md) — DELETE, GET, POST, PUT ⚠️ writes
- [CustomerReferences](fortnox-customerreferences.md) — DELETE, GET, POST, PUT ⚠️ writes
- [Customers](fortnox-customers.md) — DELETE, GET, POST, PUT ⚠️ writes
- [EUVatLimitRegulation](fortnox-euvatlimitregulation.md) — GET
- [Employees](fortnox-employees.md) — GET, POST, PUT ⚠️ writes
- [Expenses](fortnox-expenses.md) — GET, POST ⚠️ writes
- [FinanceInvoices](fortnox-financeinvoices.md) — GET, POST, PUT ⚠️ writes
- [FinancialYears](fortnox-financialyears.md) — GET, POST ⚠️ writes
- [Inbox](fortnox-inbox.md) — DELETE, GET, POST ⚠️ writes
- [InvoiceAccruals](fortnox-invoiceaccruals.md) — DELETE, GET, POST, PUT ⚠️ writes
- [InvoicePayments](fortnox-invoicepayments.md) — DELETE, GET, POST, PUT ⚠️ writes
- [Invoices](fortnox-invoices.md) — GET, POST, PUT ⚠️ writes
- [Labels](fortnox-labels.md) — DELETE, GET, POST, PUT ⚠️ writes
- [LockedPeriod](fortnox-lockedperiod.md) — GET
- [Me](fortnox-me.md) — GET
- [ModesOfPayments](fortnox-modesofpayments.md) — DELETE, GET, POST, PUT ⚠️ writes
- [Offers](fortnox-offers.md) — GET, POST, PUT ⚠️ writes
- [Orders](fortnox-orders.md) — GET, POST, PUT ⚠️ writes
- [PredefinedAccounts](fortnox-predefinedaccounts.md) — GET, PUT ⚠️ writes
- [PredefinedVoucherSeries](fortnox-predefinedvoucherseries.md) — GET, PUT ⚠️ writes
- [PriceLists](fortnox-pricelists.md) — GET, POST, PUT ⚠️ writes
- [Prices](fortnox-prices.md) — DELETE, GET, POST, PUT ⚠️ writes
- [PrintTemplates](fortnox-printtemplates.md) — GET
- [Projects](fortnox-projects.md) — DELETE, GET, POST, PUT ⚠️ writes
- [SalaryTransactions](fortnox-salarytransactions.md) — DELETE, GET, POST, PUT ⚠️ writes
- [ScheduleTimes](fortnox-scheduletimes.md) — GET, PUT ⚠️ writes
- [Sie](fortnox-sie.md) — GET
- [SupplierInvoiceAccruals](fortnox-supplierinvoiceaccruals.md) — DELETE, GET, POST, PUT ⚠️ writes
- [SupplierInvoiceExternalUrlConnections](fortnox-supplierinvoiceexternalurlconnections.md) — DELETE, GET, POST, PUT ⚠️ writes
- [SupplierInvoiceFileConnections](fortnox-supplierinvoicefileconnections.md) — DELETE, GET, POST ⚠️ writes
- [SupplierInvoicePayments](fortnox-supplierinvoicepayments.md) — DELETE, GET, POST, PUT ⚠️ writes
- [SupplierInvoices](fortnox-supplierinvoices.md) — GET, POST, PUT ⚠️ writes
- [Suppliers](fortnox-suppliers.md) — GET, POST, PUT ⚠️ writes
- [TaxReductions](fortnox-taxreductions.md) — DELETE, GET, POST, PUT ⚠️ writes
- [TermsOfDeliveries](fortnox-termsofdeliveries.md) — GET, POST, PUT ⚠️ writes
- [TermsOfPayments](fortnox-termsofpayments.md) — DELETE, GET, POST, PUT ⚠️ writes
- [TrustedEmailSenders](fortnox-trustedemailsenders.md) — DELETE, GET, POST ⚠️ writes
- [Units](fortnox-units.md) — DELETE, GET, POST, PUT ⚠️ writes
- [VacationDebtBasis](fortnox-vacationdebtbasis.md) — GET
- [VoucherFileConnections](fortnox-voucherfileconnections.md) — DELETE, GET, POST ⚠️ writes
- [VoucherSeries](fortnox-voucherseries.md) — GET, POST, PUT ⚠️ writes
- [Vouchers](fortnox-vouchers.md) — GET, POST ⚠️ writes
- [WayOfDeliveries](fortnox-wayofdeliveries.md) — DELETE, GET, POST, PUT ⚠️ writes

## integration-developer

- [Integration Ratings](integration-developer-integration-ratings.md) — GET
- [Integration Sales](integration-developer-integration-sales.md) — GET
- [Users](integration-developer-users.md) — GET

## time-reporting

- [Articles](time-reporting-articles.md) — GET
- [Registrations](time-reporting-registrations.md) — GET

## warehouse

- [CustomDocumentType](warehouse-customdocumenttype.md) — GET, POST ⚠️ writes
- [CustomInboundDocument](warehouse-custominbounddocument.md) — GET, PUT ⚠️ writes
- [CustomOutboundDocument](warehouse-customoutbounddocument.md) — GET, PUT ⚠️ writes
- [IncomingGoods](warehouse-incominggoods.md) — GET, PATCH, POST, PUT ⚠️ writes
- [ManualDocument](warehouse-manualdocument.md) — GET
- [ManualInboundDocument](warehouse-manualinbounddocument.md) — GET, PATCH, POST, PUT ⚠️ writes
- [ManualOutboundDocument](warehouse-manualoutbounddocument.md) — GET, PATCH, POST, PUT ⚠️ writes
- [ProductionOrder](warehouse-productionorder.md) — GET, PATCH, POST, PUT ⚠️ writes
- [PurchaseOrder](warehouse-purchaseorder.md) — GET, PATCH, POST, PUT ⚠️ writes
- [StockPoint](warehouse-stockpoint.md) — DELETE, GET, POST, PUT ⚠️ writes
- [StockStatus](warehouse-stockstatus.md) — GET
- [StockTaking](warehouse-stocktaking.md) — DELETE, GET, POST, PUT ⚠️ writes
- [StockTransfer](warehouse-stocktransfer.md) — GET, POST, PUT ⚠️ writes
- [Tenant](warehouse-tenant.md) — GET
