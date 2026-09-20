# Vittavaan — Page-by-Page Metric & Datapoint Dictionary

> **Purpose:** Engineering-ready inventory of the metrics and datapoints required by the 25 HTML mock pages.
>
> **Scope rule:** A datapoint is included when it is (a) visible on the page, (b) required to calculate something visible, or (c) required to support a behavior/rule explicitly represented by the page. This is not a wishlist of generic financial metrics.
>
> **Metric types**
>
> - **Source** — stored/read directly from a source, document, user input, institution, market feed, or external register.
> - **Derived** — calculated from one or more source/derived values and normally shown to the user.
> - **Hidden** — intermediate/system metric needed for calculation, ranking, validation, reconciliation, gating, or provenance.
> - **Rule/State** — categorical output or workflow state produced by business logic.

## Table of contents

1. [Advisors.dc.html](#1-advisorsdchtml)
2. [All listings.dc.html](#2-all-listingsdchtml)
3. [Analysis.dc.html](#3-analysisdchtml)
4. [Ask.dc.html](#4-askdchtml)
5. [Assets and liabilities.dc.html](#5-assets-and-liabilitiesdchtml)
6. [Attribution.dc.html](#6-attributiondchtml)
7. [Connections.dc.html](#7-connectionsdchtml)
8. [Credit.dc.html](#8-creditdchtml)
9. [Financial resume.dc.html](#9-financial-resumedchtml)
10. [Gift rules.dc.html](#10-gift-rulesdchtml)
11. [Gift transfer.dc.html](#11-gift-transferdchtml)
12. [Household.dc.html](#12-householddchtml)
13. [Inheritance.dc.html](#13-inheritancedchtml)
14. [Investor profile.dc.html](#14-investor-profiledchtml)
15. [Karjat plot.dc.html](#15-karjat-plotdchtml)
16. [Net worth.dc.html](#16-net-worthdchtml)
17. [Peers.dc.html](#17-peersdchtml)
18. [Planning.dc.html](#18-planningdchtml)
19. [Schema.dc.html](#19-schemadchtml)
20. [Settings.dc.html](#20-settingsdchtml)
21. [Stamp collection.dc.html](#21-stamp-collectiondchtml)
22. [Trends and news.dc.html](#22-trends-and-newsdchtml)
23. [User Flow.dc.html](#23-user-flowdchtml)
24. [User Story.dc.html](#24-user-storydchtml)
25. [Will.dc.html](#25-willdchtml)
26. [Cross-page core metrics](#cross-page-core-metrics)
27. [Recommended calculation conventions](#recommended-calculation-conventions)

---

## 1. `Advisors.dc.html`

**Page purpose:** Advisor marketplace, advisor matching, credentials, fees, ratings, and the user's prior/open engagements.

| Type | Metric / Datapoint | Definition / Formula | Inputs / Dependencies |
|---|---|---|---|
| Source | `AdvisorPanelCount` | Number of professionals currently on the panel | Advisor registry |
| Source | `UserAdvisorEngagementCount` | Advisors previously engaged by user | Engagement ledger |
| Derived | `AdvisorSpend12M` | Sum of payments to advisors in trailing 12 months | Advisor payment transactions |
| Source | `OpenAdvisorEngagementCount` | Number of engagements not completed/closed | Engagement status |
| Source | `EngagementDueDate` | Contracted/current due date | Engagement record |
| Derived | `DaysUntilEngagementDue` | `DueDate - CurrentDate` | Engagement due date |
| Source | `AdvisorCredentialType` | CA, SEBI RIA, registered valuer, advocate, etc. | Advisor profile |
| Rule/State | `CredentialVerificationStatus` | Whether credential has been checked against authoritative register | Credential check |
| Source | `AdvisorRating` | Displayed client rating | Rating records |
| Source | `AdvisorEngagements` | Completed engagements through platform | Engagement ledger |
| Source | `AdvisorRatedEngagements` | Engagements with a rating | Ratings |
| Derived | `RatingParticipationPct` | `RatedEngagements / Engagements` | Above |
| Source | `AdvisorFee` | Fixed/hourly fee displayed before engagement | Advisor terms |
| Source | `AdvisorSpecialties` | Property, ESOP, succession, unlisted stakes, etc. | Advisor profile |
| Hidden | `AdvisorHoldingMatch` | Intersection of advisor specialties with user's holdings/issues | Portfolio + specialties |
| Hidden | `AdvisorNeedMatch` | Whether advisor expertise matches a currently detected need | Alerts/planning + specialties |
| Rule/State | `AdvisorMatchReason` | Human-readable reason shown under “Why you are seeing them” | Match rules |
| Hidden | `AdvisorEligibility` | Advisor is verified, active, and allowed to appear | Registry + platform status |

**Important implementation note:** matching should be explainable from actual holdings/needs. Commercial placement should not silently alter `AdvisorMatchReason`.

---

## 2. `All listings.dc.html`

**Page purpose:** Marketplace inventory, filters, verification state, pricing/yield, and user threads.

| Type | Metric / Datapoint | Definition / Formula | Inputs / Dependencies |
|---|---|---|---|
| Source | `LiveListingCount` | Number of active marketplace listings | Listing status |
| Derived | `LiveAssetClassCount` | Distinct asset classes among live listings | Listings |
| Derived | `MatchingListingCount` | Listings satisfying active filters | Filter engine |
| Derived | `MatchingPriceMin` | Minimum asking price among matching listings | Filtered listings |
| Derived | `MatchingPriceMax` | Maximum asking price among matching listings | Filtered listings |
| Derived | `FullyVerifiedListingCount` | Matching listings where all required checks passed | Verification checks |
| Derived | `FullyVerifiedListingPct` | `FullyVerified / MatchingListingCount` | Above |
| Source | `ActiveThreadCount` | User's open buyer/seller threads | Messaging/transaction state |
| Derived | `DaysAwaitingUserReply` | Days since counterparty message requiring user response | Thread timestamps |
| Derived | `ListingCountByAssetClass` | Active listings grouped by class | Listings |
| Source | `ListingAskingPrice` | Seller's asking price | Listing |
| Source | `ListingMonthlyRent` | Contracted rent in place | Lease/listing docs |
| Derived | `ListingAnnualRent` | `MonthlyRent × 12` unless actual schedule differs | Rent |
| Derived | `GrossYieldOnAsking` | `AnnualRent / AskingPrice` | Rent + asking price |
| Source | `AnnualRentEscalationPct` | Contractual escalation | Lease |
| Source | `ListingArea` | Sq ft / other area | Listing docs |
| Derived | `AskingPricePerArea` | `AskingPrice / Area` | Price + area |
| Rule/State | `ListingVerificationStatus` | All passed / some open / unchecked | Required check set |
| Derived | `VerificationCompletionPct` | `PassedRequiredChecks / RequiredChecks` | Check ledger |
| Source | `ListingDate` | Date listing went live | Listing |
| Derived | `DaysListed` | `CurrentDate - ListingDate` | Listing date |
| Source | `SellerFeePct` | Platform fee on completion | Marketplace fee schedule |
| Derived | `SellerFeeAmount` | `CompletionPrice × SellerFeePct` | Deal price + fee |
| Hidden | `FilterExclusionCount` | Listings removed by user exclusions | Filter engine |
| Hidden | `SortKey` | Newest/price/yield/verification selected by user | UI state |

---

## 3. `Analysis.dc.html`

**Page purpose:** Portfolio return analysis over selectable windows.

| Type | Metric / Datapoint | Definition / Formula | Inputs / Dependencies |
|---|---|---|---|
| Source | `PerformanceAsOf` | Pricing timestamp for performance calculations | Valuation layer |
| Derived | `PortfolioXIRR` | Money-weighted annualized return from dated external cash flows and terminal value | Transactions + valuations |
| Derived | `PortfolioTWRR` | Geometrically linked sub-period returns neutralizing external flows | Daily/sub-period valuations + flows |
| Derived | `BenchmarkReturn` | Return of specified blended benchmark over same period | Benchmark series |
| Derived | `ExcessReturnVsBenchmarkPts` | `PortfolioTWRR - BenchmarkReturn` when comparing portfolio skill to benchmark | TWRR + benchmark |
| Derived | `MaxDrawdownPct` | Maximum peak-to-trough decline | Portfolio value series |
| Source/Derived | `DrawdownStartDate` | Date of prior peak | Value series |
| Source/Derived | `DrawdownTroughDate` | Date of trough | Value series |
| Derived | `DrawdownRecoveryMonths` | Months from trough/peak definition to recovery of prior high | Value series |
| Derived | `AssetClassAvgWeight` | Time-weighted average class allocation over period | Historical holdings |
| Derived | `AssetClassContributionPts` | Contribution of asset class to portfolio return | Attribution engine |
| Derived | `AssetClassIncomeYield` | Income generated / relevant average asset value | Income streams + values |
| Rule/State | `PerformanceBasis` | Verified / estimated / self-declared | Valuation provenance |
| Derived | `EstimatedValueContributionPts` | Return points dependent on estimated property values | Attribution + provenance |
| Derived | `ReturnExcludingEstimatedValues` | Recomputed return excluding designated estimated/self-declared valuation effects | Performance engine |
| Source | `Crypto12MReturn` | 12-month return for crypto line | User/exchange price history |
| Derived | `PortfolioHoldingCost` | Fund expenses + brokerage/taxes + property holding costs + other included costs | Cost ledger |
| Derived | `PortfolioCostRatio` | `IncludedHoldingCosts / AverageRelevantAssets` | Costs + average assets |

**Key distinction:** XIRR and TWRR answer different questions and should never be used interchangeably.

---

## 4. `Ask.dc.html`

**Page purpose:** Natural-language answers grounded in the user's ledger and named sources.

| Type | Metric / Datapoint | Definition / Formula | Inputs / Dependencies |
|---|---|---|---|
| Source | `QuestionPeriodStart` | Start date inferred/selected for question | Query parser |
| Source | `QuestionPeriodEnd` | End/as-of date | Query parser |
| Derived | `PropertyCashInvested` | Cash invested into selected property during period | Transactions |
| Derived | `RentReceived` | Sum of actual rent received during period | Bank/rent ledger |
| Derived | `RentMonthsReceived` | Count of months with actual rent receipt | Rent ledger |
| Derived | `ExpectedRentMonths` | Months property was expected to be occupied/earning | Lease/occupancy |
| Derived | `MissingRentMonths` | Expected months without receipt | Above |
| Derived | `PropertyTaxAndDues` | Sum of property tax + society/association dues | Documents + transactions |
| Derived | `RepairAndRefurbishmentCost` | Sum of tagged repair/refurbishment transactions | Transaction categorization |
| Derived | `AttributedLoanInterest` | Interest attributable to selected property | Loan schedule + attribution rule |
| Derived | `RecordedValueChange` | `EndRecordedValue - StartRecordedValue` | Property valuations |
| Derived | `PropertyNetEconomicGain` | `Rent - costs - attributed interest + recorded value change` | Above |
| Derived | `PropertyAnnualizedReturn` | Annualized return on opening capital using defined methodology | Opening value + flows + gain |
| Derived | `RentOnlyYield` | Rental return excluding property revaluation | Rent + capital base |
| Source | `AnswerSourceCount` | Number of documents/feeds used | Provenance graph |
| Source | `AnswerSourceAsOf` | Freshness date per source | Source metadata |
| Rule/State | `AnswerConfidenceDisclosure` | Flags estimated, missing, or self-declared components | Provenance + completeness |
| Hidden | `ExcludedMissingDataValue` | Missing observations excluded rather than imputed | Data quality rules |

---

## 5. `Assets and liabilities.dc.html`

**Page purpose:** Multi-tab portfolio ledger covering net worth, assets, liabilities, cash flow, data room and consents.

### Net worth tab

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Derived | `TotalAssets` | Sum of current attributable asset values |
| Derived | `TotalLiabilities` | Sum of current outstanding liabilities |
| Derived | `NetWorth` | `TotalAssets - TotalLiabilities` |
| Derived | `NetWorthChangeAmount` | `CurrentNetWorth - PriorPeriodNetWorth` |
| Derived | `NetWorthChangePct` | `NetWorthChangeAmount / PriorPeriodNetWorth` |
| Derived | `MonthlyAssets` | Assets at each month-end |
| Derived | `MonthlyLiabilities` | Liabilities at each month-end |
| Derived | `MonthlyNetWorth` | `MonthlyAssets - MonthlyLiabilities` |
| Derived | `MonthlyNetWorthChange` | Current month net worth minus prior month |
| Derived | `EquityGainContribution` | Net-worth movement attributable to equity price gains |
| Derived | `RealEstateRevaluationContribution` | Movement attributable to changed property marks |
| Derived | `FreshInvestmentContribution` | External capital contributed |
| Derived | `LoanRepaymentContribution` | Net-worth effect of principal repayment |
| Derived | `CryptoChangeContribution` | Net-worth movement attributable to crypto |
| Hidden | `MovementReconciliation` | Sum of movement components; must reconcile to total change |

### Assets tab

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `AssetQuantity` | Units/shares/weight/ownership quantity |
| Source | `AssetCurrentPrice` | Current unit price/valuation |
| Derived | `AssetCurrentValue` | Quantity × price, or approved valuation |
| Source | `AssetCostBasis` | Adjusted acquisition cost |
| Derived | `AssetGainAmount` | `CurrentValue - CostBasis` |
| Derived | `AssetGainPct` | `GainAmount / CostBasis` |
| Derived | `AssetClassValue` | Sum by asset class |
| Derived | `AssetClassSharePct` | `ClassValue / TotalAssets` |
| Derived | `HoldingSharePct` | `HoldingValue / TotalAssets` |
| Source | `OwnershipPct` | Legal/economic ownership share |
| Derived | `AttributedAssetValue` | `GrossAssetValue × OwnershipPct` |
| Source | `ValuationAsOf` | Date/time of valuation |
| Source | `ValuationMethod` | Market feed, circle rate, appraisal, last round, cost, manual estimate |
| Rule/State | `VerificationLevel` | Self-declared/documented/verified/accepted |
| Derived | `ValuationAgeDays` | Current date minus valuation date |
| Rule/State | `StalenessStatus` | Fresh/stale based on asset-specific window |

### Liabilities tab

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `OriginalLoanAmount` | Original facility amount |
| Source | `OutstandingPrincipal` | Current unpaid principal |
| Source | `InterestRate` | Current nominal rate |
| Source | `RateType` | Fixed/floating |
| Source | `RemainingTenure` | Remaining term |
| Derived | `LiabilitySharePct` | `Outstanding / TotalLiabilities` |
| Derived | `PrincipalPaidToDate` | Original principal adjusted for redraws minus outstanding |
| Derived | `InterestPaidToDate` | Sum of interest payments |
| Derived | `DebtChangeAmount` | Current outstanding minus prior-period outstanding |
| Derived | `LoanToLinkedAssetValue` | `Outstanding / LinkedCollateralValue` |
| Source | `PaymentDueDate` | Next scheduled payment |
| Derived | `ScheduledDebtService` | Sum of required payments over selected period |

### Cash flow tab

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Derived | `MonthlyInflows` | Sum of classified inflows |
| Derived | `MonthlyOutflows` | Sum of classified outflows |
| Derived | `MonthlySurplus` | `Inflows - Outflows` |
| Derived | `SavingsRate` | `MonthlySurplus / MonthlyInflows` |
| Derived | `IncomeBySource` | Inflows grouped by salary/rent/dividend/etc. |
| Derived | `ExpenseByCategory` | Outflows grouped by category |
| Derived | `ExpenseCategoryPct` | `CategoryOutflow / TotalOutflow` |
| Derived | `DebtServiceRatio` | `DebtService / DefinedIncomeBase` |
| Hidden | `UnclassifiedTransactionCount` | Transactions not assigned to a category |
| Hidden | `CashFlowCoveragePct` | Share of expected transaction sources successfully represented |

### Data room / consents

Required datapoints include `DocumentType`, `DocumentOwner`, `DocumentAssetLink`, `DocumentDate`, `DocumentExpiry`, `ConsentSource`, `ConsentScope`, `ConsentPurpose`, `ConsentGrantedAt`, `ConsentExpiresAt`, `ConsentRevokedAt`, and `ConsentStatus`.

---

## 6. `Attribution.dc.html`

**Page purpose:** Explain where return came from by asset class, sector and holding, using fair benchmarks.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Derived | `PeriodPortfolioReturn` | Portfolio return for selected period |
| Derived | `PeriodGainAmount` | Rupee gain over selected period |
| Derived | `Nifty500TRIReturn` | Equity benchmark return for same period |
| Derived | `GapVsEquityBenchmark` | Portfolio return minus Nifty 500 TRI return |
| Derived | `BlendedBenchmarkReturn` | Benchmark rebuilt from portfolio allocation weights |
| Derived | `GapVsBlendedBenchmark` | Portfolio return minus blended benchmark |
| Derived | `StartPeriodAssetClassWeight` | Class value / total at start of period |
| Derived | `AssetClassPeriodReturn` | Class return over period |
| Derived | `AssetClassGainAmount` | Rupee gain by class |
| Derived | `AssetClassContributionPct` | Contribution of class to cumulative portfolio return |
| Hidden | `ContributionReconciliation` | Sum of class contributions equals portfolio cumulative return |
| Derived | `UnderlyingSectorExposureValue` | Direct + fund look-through exposure to sector |
| Derived | `UnderlyingSectorExposurePct` | `SectorExposure / LookThroughPortfolioBase` |
| Derived | `SectorReturn` | Return of underlying sector exposure over period |
| Derived | `SectorContribution` | Sector's contribution to portfolio return |
| Derived | `DirectSecurityExposure` | Direct value in security |
| Derived | `IndirectSecurityExposure` | Look-through exposure through funds |
| Derived | `EffectiveSecurityExposure` | Direct + indirect exposure |
| Derived | `EffectiveSecurityExposurePct` | Effective exposure / portfolio base |
| Derived | `FundOverlapSecurityCount` | Number of underlying securities shared by selected funds |
| Derived | `FundOverlapValue` | Effective duplicated economic exposure |
| Hidden | `BenchmarkWeightSeries` | Monthly/time-series weights used to rebuild blended benchmark |

---

## 7. `Connections.dc.html`

**Page purpose:** Connected institutions, source coverage, freshness, verification and consent health.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `ConnectionCount` | Number of configured source connections |
| Derived | `ActiveConnectionCount` | Connections currently authorized and functioning |
| Derived | `FailedConnectionCount` | Connections currently failing |
| Source | `LastSuccessfulSyncAt` | Most recent successful source sync |
| Derived | `DaysSinceLastSync` | Current time minus last successful sync |
| Rule/State | `ConnectionFreshnessStatus` | Fresh/stale/down based on source-specific rules |
| Source | `ConsentGrantedAt` | Consent start |
| Source | `ConsentExpiresAt` | Consent expiry |
| Derived | `DaysUntilConsentExpiry` | Expiry minus current date |
| Source | `ConsentScope` | Data/actions source is allowed to provide |
| Source | `ConsentPurpose` | Recorded purpose |
| Rule/State | `ConsentStatus` | Active/expired/revoked |
| Derived | `VerifiedValue` | Wealth value supported by verified sources |
| Derived | `SelfDeclaredValue` | Wealth value relying on self-declaration |
| Derived | `VerifiedWealthPct` | `VerifiedValue / NetWorth` using page's defined basis |
| Derived | `ConnectedValueCoveragePct` | Value represented by functioning connected sources / relevant total |
| Derived | `SourceCoverageCount` | Expected sources represented |
| Hidden | `MissingSourceCount` | Expected sources not connected/readable |
| Hidden | `SourceErrorAge` | Duration of current connection failure |

---

## 8. `Credit.dc.html`

**Page purpose:** Anonymous credit request, black-box borrower profile, lender bidding, consent and handover.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `RequestedCreditAmount` | Amount user wants to raise |
| Derived | `IndicativeCreditCeiling` | Platform-calculated indicative maximum based on permitted underwriting inputs |
| Source | `CreditPurpose` | Working capital/property/refinance/etc. |
| Source | `RequestedTenure` | Desired term |
| Source | `OfferedSecurityClasses` | Asset classes user permits as security |
| Derived | `EligibleSecurityValue` | Verified/accepted value eligible for lender use |
| Source | `BorrowerReference` | Anonymous platform reference |
| Derived | `VerifiedNetWorth` | Net worth restricted to qualifying verification levels |
| Derived | `VerifiedAnnualIncome` | Annual income supported by qualifying sources |
| Source | `CIBILScore` | Bureau score and pull date |
| Source | `CRIFScore` | Bureau score and pull date |
| Source | `AgeBand` | Privacy-preserving age bucket |
| Source | `CityTier` | Privacy-preserving location category |
| Source | `IncomeType` | Salaried/rental/dividend/etc. |
| Derived | `EmploymentTenureYears` | Years in employment history |
| Derived | `EmployerCount` | Distinct employers over defined history |
| Derived | `ExistingDebtServiceRatio` | Required debt payments / defined verified income |
| Derived | `OnTimeInstallmentCount` | Instalments paid on/before due date |
| Derived | `TotalInstallmentCount` | Instalments evaluated |
| Derived | `OnTimePaymentPct` | `OnTime / Total` |
| Derived | `CreditUtilisationPct` | Revolving balance / available revolving limit |
| Derived | `RecentCreditEnquiryCount` | Bureau enquiries within window |
| Derived | `LiquidAssets` | Assets meeting liquidity definition |
| Source/Derived | `ContingentLiabilities` | Guarantees/other contingent obligations |
| Derived | `SecurityCoverMultiple` | `EligibleSecurityValue / RequestedCreditAmount` |
| Derived | `MatchingLenderCount` | Empanelled lenders eligible for request |
| Derived | `MatchingBankCount` | Matching banks |
| Derived | `MatchingNBFCCount` | Matching NBFCs |
| Derived | `MatchingPrivateBankCount` | Matching wealth/private banks |
| Source | `BidRate` | Lender bid interest rate |
| Source | `BidFees` | Processing/other lender fees |
| Derived | `BidAPR` | Effective annual borrowing cost using rate + mandatory fees |
| Derived | `BidEMI` | Scheduled payment from amount/rate/tenure |
| Derived | `BidTotalInterest` | Total scheduled interest |
| Derived | `BidTotalRepayment` | Principal + interest + included fees |
| Derived | `BidExpiryAt` | Deadline for accepting bid |
| Hidden | `ReIdentificationRisk` | Privacy-risk check from combination of published characteristics |
| Rule/State | `IdentityReleaseStatus` | Identity withheld until user chooses and consents |

---

## 9. `Financial resume.dc.html`

**Page purpose:** Shareable, attested financial standing with recipient-specific disclosure controls.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Derived | `IndividualNetWorth` | User-attributable assets minus user-attributable liabilities |
| Derived | `VerifiedNetWorth` | Portion of net worth meeting verification rule |
| Derived | `UnverifiedNetWorth` | Individual net worth not meeting verification rule |
| Derived | `HouseholdNetWorth` | Household assets minus household liabilities |
| Derived | `AnnualIncome` | Annualized/actual income from defined sources |
| Derived | `IncomeBySource` | Salary, rent share, dividends, interest, etc. |
| Derived | `DebtServiceRatio` | Scheduled debt service / income |
| Derived | `AnnualDebtService` | Annual required debt payments |
| Derived | `Liquidity3Day` | Value realizable within three days under definition |
| Derived | `Liquidity1Year` | Value realizable within one year |
| Derived | `IlliquidValue` | Assets outside liquidity buckets |
| Derived | `OnTimePaymentRecord` | On-time instalments / evaluated instalments |
| Derived | `CurrentFacilityCount` | Active credit facilities |
| Derived | `OverdueFacilityCount` | Facilities with overdue amount |
| Derived | `CreditUtilisationPct` | Revolving balance / limit |
| Derived | `RecentEnquiryCount` | Bureau enquiries in defined window |
| Source | `BureauScores` | CIBIL/CRIF scores + pull dates |
| Derived | `YearsInvested` | Years since first qualifying investment |
| Derived | `AssetClassesHeldCount` | Distinct asset classes held |
| Derived | `SyndicateInvestmentCount` | Count of qualifying syndicate investments |
| Derived | `SyndicateExitCount` | Completed exits |
| Derived | `ExitMultiple` | Exit proceeds / invested capital for an exit |
| Derived | `VerifiedAssetPct` | Verified asset value / total relevant assets |
| Derived | `LargestHoldingPct` | Largest single holding / own assets |
| Derived | `LargestIssuerExposurePct` | Largest issuer exposure including fund look-through |
| Derived | `PropertyConcentrationPct` | Property value / total relevant assets |
| Derived | `DirectSourceAccountCount` | Accounts read directly |
| Derived | `SourceFreshnessMinDays` | Freshest source age |
| Derived | `SourceFreshnessMaxDays` | Oldest source age |
| Source | `AttestorName` | Named professional attesting document |
| Source | `AttestationDate` | Date of attestation |
| Derived | `SharedFieldCount` | Number of available resume fields included in current share |
| Rule/State | `RecipientDisclosureSet` | Exact fields recipient is permitted to see |

---

## 10. `Gift rules.dc.html`

**Page purpose:** Rules engine explaining who can receive a gift, tax treatment, asset eligibility and transfer mechanism.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `Donor` | Person/entity making gift |
| Source | `Recipient` | Person/entity receiving gift |
| Source | `RelationshipToRecipient` | Relationship evaluated from receiver's side |
| Source | `GiftAsset` | Asset proposed for transfer |
| Derived | `GiftValue` | Value used for tax/rule evaluation |
| Rule/State | `RelativeExemptionStatus` | Exempt/taxable/disputed under encoded relationship rule |
| Source | `NonRelativeGiftThreshold` | Applicable annual threshold |
| Derived | `TaxableGiftAmount` | Amount subject to recipient income tax under applicable rule |
| Rule/State | `AssetGiftEligibility` | Whether donor legally/economically owns transferable interest |
| Rule/State | `JointAssetRestriction` | Whether co-owner consent/partial transfer rules apply |
| Rule/State | `PledgeRestriction` | Whether pledged/encumbered asset can be gifted |
| Rule/State | `ProductTransferRestriction` | EPF/unvested option/etc. restrictions |
| Rule/State | `NomineeOwnershipMismatch` | User is nominee but not owner |
| Source | `AssetOwnershipPct` | Donor's transferable ownership share |
| Derived | `MaximumGiftableValue` | Value of legally transferable ownership interest |
| Rule/State | `TransferMechanism` | Nominee/gift/will/inheritance |
| Hidden | `RuleJurisdiction` | Jurisdiction governing rule |
| Hidden | `RuleEffectiveDate` | Effective date/version of tax/legal rule |
| Hidden | `RuleConfidenceStatus` | Settled/disputed/needs professional confirmation |

---

## 11. `Gift transfer.dc.html`

**Page purpose:** Execute and track a specific family gift from planning through registration and mutation.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `GiftAssetValue` | Value of asset being transferred |
| Source | `DonorOwnershipPct` | Donor's ownership before gift |
| Source | `RecipientRelationship` | Relationship used for tax/stamp-duty rules |
| Rule/State | `RecipientGiftTaxStatus` | Exempt/taxable based on relationship and law version |
| Source | `OriginalAcquisitionDate` | Donor's original acquisition date |
| Source | `OriginalCostBasis` | Donor's adjusted cost basis |
| Derived | `RecipientCarriedCostBasis` | Cost basis carried to recipient where applicable |
| Derived | `RecipientHoldingPeriodStart` | Original acquisition date where holding period carries over |
| Source | `StampDutyRate` | Applicable rate/concession |
| Derived | `StampDutyAmount` | Applicable value base × duty rate |
| Source | `RegistrationFee` | Registration charge |
| Source | `LegalFee` | Advocate/documentation fee |
| Source | `OtherTransferCost` | Other required transfer costs |
| Derived | `TotalTransferCost` | Sum of transfer costs |
| Derived | `TransferCostPct` | `TotalTransferCost / GiftAssetValue` |
| Derived | `FamilyConcessionSaving` | Standard duty/cost minus concessionary duty/cost |
| Rule/State | `GiftDeedStatus` | Drafted/signed/registered/etc. |
| Source | `RegistrationDate` | Registration date |
| Rule/State | `MutationStatus` | Pending/completed/rejected |
| Source | `MutationDate` | Date title/record mutation completed |
| Derived | `DaysToMutation` | Mutation date minus registration date |
| Rule/State | `PortfolioOwnershipUpdateStatus` | Whether ledger ownership has been updated after legal completion |
| Hidden | `TransferChecklistCompletionPct` | Completed required steps / total required steps |

---

## 12. `Household.dc.html`

**Page purpose:** Household-level balance sheet, member attribution, income/outgoings, ownership and cross-member obligations.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Derived | `HouseholdAssets` | Sum of assets once at household level |
| Derived | `HouseholdLiabilities` | Sum of liabilities once at household level |
| Derived | `HouseholdNetWorth` | `HouseholdAssets - HouseholdLiabilities` |
| Derived | `MemberAttributedAssets` | Sum of asset values × member ownership shares |
| Derived | `MemberAttributedLiabilities` | Liabilities attributable to member |
| Derived | `MemberNetWorth` | Member assets minus member liabilities |
| Derived | `MemberHouseholdNetWorthShare` | `MemberNetWorth / HouseholdNetWorth` |
| Source | `OwnershipSplitPct` | Legal/economic ownership per member/entity |
| Derived | `JointHoldingAttributedValue` | `JointAssetValue × MemberOwnershipPct` |
| Hidden | `HouseholdDeduplicatedAssetValue` | Prevents joint assets being counted twice |
| Hidden | `HouseholdDeduplicatedLiabilityValue` | Prevents joint debt double counting |
| Derived | `HouseholdMonthlyIncome` | Sum of household inflows |
| Derived | `HouseholdMonthlyOutflow` | Sum of household outflows |
| Derived | `HouseholdMonthlySurplus` | Income minus outflow |
| Derived | `HouseholdPassiveIncome` | Rent + dividends + interest + other defined passive income |
| Derived | `PassiveIncomePct` | `PassiveIncome / HouseholdIncome` |
| Derived | `HouseholdDebtService` | Scheduled household debt payments |
| Derived | `HouseholdDebtServiceRatio` | Debt service / household income |
| Derived | `DependentSupportAmount` | Transfers/support tagged to dependants |
| Source | `HouseholdRole` | Owner/admin/guardian/dependant/etc. |
| Rule/State | `MemberAccessScope` | Data/actions a member may access |

---

## 13. `Inheritance.dc.html`

**Page purpose:** Model what happens to assets on death, including nominations, will, succession and settlement.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Derived | `GrossEstateValue` | Current value of assets included in estate |
| Derived | `EstateLiabilities` | Liabilities/claims payable by estate |
| Derived | `NetEstateValue` | `GrossEstateValue - EstateLiabilities` |
| Source | `Beneficiary` | Person/entity receiving under will/rule |
| Source | `BeneficiarySharePct` | Share specified by will/rule |
| Derived | `BeneficiaryShareValue` | `NetDistributableEstate × SharePct` |
| Source | `Nominee` | Nominee recorded on asset/account |
| Rule/State | `NomineeBeneficiaryMismatch` | Nominee differs from beneficial successor |
| Rule/State | `WillCoverageStatus` | Asset covered/uncovered/ambiguous |
| Derived | `WillCoveredEstateValue` | Estate value with valid disposition |
| Derived | `IntestateEstateValue` | Estate value without effective disposition |
| Derived | `EstateCoveragePct` | `CoveredEstateValue / GrossEstateValue` |
| Rule/State | `DefaultSuccessionRule` | Applicable intestacy rule |
| Derived | `DefaultInheritanceSharePct` | Share under applicable succession rule |
| Derived | `DefaultInheritanceValue` | Estate × default share |
| Derived | `IntendedVsDefaultDifference` | Intended value minus default-rule value |
| Source | `InheritedCostBasis` | Cost basis used by successor under applicable rule |
| Source/Derived | `InheritedHoldingPeriodStart` | Holding-period start carried under tax rule |
| Rule/State | `SuccessionDocumentRequirement` | Probate/succession certificate/etc. as applicable |
| Derived | `EstateDistributionCompletionPct` | Distributed/resolved estate items / required items |
| Derived | `EstateSettlementDays` | Settlement date minus death/estate-start date |
| Hidden | `OutstandingEstateIssueCount` | Unresolved title, nominee, document, tax or distribution items |

---

## 14. `Investor profile.dc.html`

**Page purpose:** Explain investor characteristics without collapsing everything into one opaque risk score.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `ProfileAnswer` | User response to each profile question |
| Source | `ProfileAnswerWeight` | Weight/logic attached to response where applicable |
| Derived | `RiskCapacityScore` | Ability to bear financial loss based on objective financial factors |
| Derived | `RiskToleranceScore` | Willingness to accept volatility/loss based on responses |
| Derived | `LiquidityNeedScore` | Degree of near-term cash need |
| Derived | `InvestmentHorizonScore` | Time-horizon dimension |
| Derived | `IncomeStabilityScore` | Stability/diversification of income |
| Derived | `LossReactionScore` | Behavioral response to drawdown scenarios |
| Derived | `InvestmentKnowledgeScore` | Familiarity/experience dimension |
| Derived | `ConcentrationToleranceScore` | Stated comfort with concentrated positions |
| Derived | `ObservedConcentrationPct` | Actual concentration from holdings |
| Derived | `ObservedLiquidityPct` | Liquid assets / relevant assets |
| Derived | `ObservedDebtServiceRatio` | Debt service / income |
| Rule/State | `ProfileClassification` | Explainable profile/bucket derived from defined dimensions |
| Hidden | `CapacityToleranceConflict` | Flags material disagreement between ability and willingness |
| Source | `ProfileCreatedAt` | Initial profile date |
| Source | `ProfileLastReviewedAt` | Last review date |
| Derived | `DaysSinceProfileReview` | Current date minus review date |
| Hidden | `ProfileVersion` | Version of questionnaire/scoring logic |

---

## 15. `Karjat plot.dc.html`

**Page purpose:** Specific real-estate asset transaction/ownership page with due diligence, valuation and transfer history.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `PurchasePrice` | Contract purchase consideration |
| Source | `StampDuty` | Duty paid |
| Source | `RegistrationCost` | Registration fee |
| Source | `LegalDueDiligenceCost` | Legal/title diligence cost |
| Source | `OtherAcquisitionCost` | Other capitalizable acquisition costs |
| Derived | `TotalAcquisitionCost` | Purchase price + capitalizable acquisition costs |
| Derived | `PropertyCostBasis` | Adjusted tax/accounting basis per applicable rules |
| Source | `PropertyArea` | Plot area |
| Derived | `AcquisitionPricePerArea` | Purchase price / area |
| Source | `CurrentEstimatedValue` | Latest valuation/estimate |
| Derived | `EstimatedUnrealizedGain` | Current estimate minus adjusted cost basis |
| Derived | `EstimatedUnrealizedGainPct` | Gain / cost basis |
| Source | `ValuationMethod` | Circle rate/comparable/appraisal/user estimate |
| Source | `ValuationAsOf` | Valuation date |
| Derived | `ValuationAgeDays` | Current date minus valuation date |
| Rule/State | `ValuationStalenessStatus` | Fresh/stale per property rule |
| Source | `ComparableLow` | Low comparable transaction/valuation |
| Source | `ComparableHigh` | High comparable |
| Derived | `ComparableMedian` | Median of valid comparables |
| Derived | `ComparablePricePerArea` | Comparable value / comparable area |
| Rule/State | `TitleVerificationStatus` | Title checks completed/passed |
| Rule/State | `EncumbranceStatus` | Encumbered/clear/unknown |
| Rule/State | `MutationStatus` | Land-record mutation state |
| Source | `OwnershipPct` | Ownership share |
| Derived | `AttributedPropertyValue` | Gross value × ownership share |
| Source | `RegistrationDate` | Date registered |
| Derived | `HoldingPeriodDays` | Current date minus acquisition/recognized holding start |
| Hidden | `DocumentChecklistCompletionPct` | Required property documents completed / required |

---

## 16. `Net worth.dc.html`

**Page purpose:** Main household overview: wealth, verification, movers, ownership, debt, income/outgoings and alerts.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Derived | `NetWorth` | `TotalAssets - TotalLiabilities` |
| Derived | `NetWorthMoMChangeAmount` | Current net worth minus prior month |
| Derived | `NetWorthMoMChangePct` | MoM change / prior-month net worth |
| Derived | `TotalAssets` | Sum of attributable asset values |
| Derived | `AssetMoMChangeAmount` | Current assets minus prior month |
| Derived | `AssetMoMChangePct` | Asset change / prior-month assets |
| Derived | `TotalLiabilities` | Sum of outstanding liabilities |
| Derived | `LiabilityMoMChangeAmount` | Current liabilities minus prior month |
| Derived | `LiabilityMoMChangePct` | Liability change / prior-month liabilities |
| Derived | `VerifiedNetWorth` | Net worth supported by qualifying verified values |
| Derived | `VerifiedWealthPct` | `VerifiedNetWorth / NetWorth` |
| Derived | `SelfDeclaredNetWorth` | Net worth attributable to self-declared components |
| Derived | `NetWorth12MChangeAmount` | Current minus 12-month-prior net worth |
| Derived | `NetWorth12MChangePct` | 12M change / starting net worth |
| Derived | `Asset12MChangeAmount` | Asset change over 12 months |
| Derived | `Debt12MChangeAmount` | Liability change over 12 months |
| Rule/State | `NetWorthSeriesPartial` | Historical line has stale/missing valuations |
| Hidden | `InterpolationUsed` | Must be false where page explicitly says feed outage not interpolated |
| Derived | `Holding12MChangePct` | Holding/class value change over trailing 12 months |
| Derived | `AssetClassValue` | Sum by displayed class |
| Derived | `AssetClassSharePct` | Class value / total assets |
| Derived | `LiabilitySharePct` | Liability outstanding / total liabilities |
| Derived | `MonthlyIncomeBySource` | Current-month inflows grouped by source |
| Derived | `MonthlyTotalIncome` | Sum of current-month inflows |
| Derived | `MonthlyExpenseByCategory` | Current-month outflows grouped by category |
| Derived | `MonthlyTotalOutflow` | Sum of current-month outflows |
| Derived | `ExpensePctOfIncome` | Category amount / total monthly income |
| Derived | `MonthlySurplus` | Total income minus total outflow |
| Derived | `FundOverlapCount` | Number of common underlying stocks across selected funds |
| Derived | `CashYieldPct` | Annual interest earned / average cash balance |
| Derived | `EmployerExposurePct` | Direct + indirect employer exposure / household assets |
| Hidden | `AlertMaterialityScore` | Used to select “Worth a look” items |
| Hidden | `AlertEvidence` | Holdings/transactions supporting each alert |

---

## 17. `Peers.dc.html`

**Page purpose:** Consent-based peer/circle sharing, personas, requests and privacy boundaries — not ranking.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Derived | `PeopleSharingWithUserCount` | People with at least one active grant to user |
| Derived | `LivePersonaCount` | User personas currently active |
| Derived | `ReciprocalGrantCount` | People user also shares something with |
| Derived | `ReciprocityPct` | `ReciprocalGrantCount / PeopleSharingWithUserCount` |
| Source | `GrantDepth` | Full/scoped/single asset/band/one field |
| Source | `GrantFields` | Exact fields shared |
| Source | `GrantStartDate` | Consent/grant date |
| Source | `GrantExpiryDate` | Expiry or standing |
| Derived | `DaysUntilGrantExpiry` | Expiry minus current date |
| Source | `LastViewedAt` | Last time recipient viewed grant |
| Derived | `SharedFieldCount` | Number of fields exposed by a grant |
| Derived | `WithheldFieldCount` | Available fields explicitly withheld |
| Source | `NetWorthBand` | Privacy-preserving wealth band where exact amount withheld |
| Derived | `PublishedAssetMixPct` | Percent allocation by class where permitted |
| Derived | `GoalProgressPct` | Progress shown where grant includes goals |
| Source | `PendingAccessRequestCount` | Requests awaiting user action |
| Derived | `RequestAgeDays` | Current date minus request date |
| Rule/State | `RequestExpiryDate` | Auto-expiry under platform rule |
| Hidden | `ConsentCapabilitySet` | Server-side fields/actions permitted by grant |
| Rule/State | `SensitiveUserSafeguard` | Additional review/guardrails where consent quality may be questionable |

**Do not create:** peer leaderboard, peer score, “better/worse” ranking, or automatic trade-copy metric; the page explicitly rejects those behaviors.

---

## 18. `Planning.dc.html`

**Page purpose:** Goals, funding, assumptions, upcoming financial events and calculators.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `EquityReturnAssumption` | Planning assumption |
| Source | `DebtReturnAssumption` | Planning assumption |
| Source | `InflationAssumption` | Planning assumption |
| Derived | `CommittedToGoalsValue` | Current value earmarked to named goals |
| Derived | `CommittedToGoalsPct` | `CommittedValue / NetWorth` (per mock basis) |
| Derived | `UnallocatedValue` | Net worth/eligible wealth not attached to goals |
| Derived | `GoalsOnTrackCount` | Goals whose projected funding meets/exceeds need under assumptions |
| Source | `GoalTargetYear` | Year/date goal requires funds |
| Derived | `GoalNeededThen` | Inflation-adjusted/defined target amount at target date |
| Derived | `GoalFundedToday` | Current value of holdings assigned to goal |
| Derived | `GoalProjectedValue` | Future value of assigned holdings + recorded additions under assumptions |
| Derived | `GoalFundingGap` | `GoalNeededThen - GoalProjectedValue` |
| Derived | `GoalFundingPct` | `GoalProjectedValue / GoalNeededThen` |
| Rule/State | `GoalStatus` | On track/short/funded/dependent on uncertain exit/etc. |
| Derived | `AccessibleGoalFundingByDate` | Portion of assigned funding legally/liquidly accessible by goal date |
| Derived | `TimingMismatchAmount` | Funding value not available when goal requires it |
| Source | `UpcomingFinancialEventDate` | Lease renewal, ESOP window, insurance renewal, age milestone |
| Derived | `DaysUntilFinancialEvent` | Event date minus current date |
| Source | `LoanPrepaymentAmount` | Calculator input |
| Source | `LoanRate` | Current facility rate |
| Source | `InvestmentReturnAssumption` | Calculator input |
| Derived | `InterestAvoidedByPrepayment` | Interest saved under amortization schedule |
| Derived | `InvestmentFutureValue` | Future value of alternative investment |
| Derived | `EstimatedTaxOnInvestmentGain` | Tax on modeled investment gain under stated rule |
| Derived | `PrepayNetPosition` | Economic end-position under prepayment scenario |
| Derived | `InvestNetPosition` | Economic end-position under investment scenario |
| Derived | `ScenarioDifference` | Invest position minus prepay position |
| Derived | `CrossoverReturn` | Assumed investment return at which modeled end positions are equal |
| Hidden | `ProjectionAssumptionSetVersion` | Version of assumptions/rules used for saved plan |

---

## 19. `Schema.dc.html`

**Page purpose:** Engineering/data-model specification rather than a consumer financial screen. Metrics here are primarily canonical fields and calculation-support datapoints.

### Core canonical datapoints

`PersonId`, `HouseholdId`, `MembershipId`, `EntityId`, `EntityType`, `EntityRole`, `AccessGrantId`, `SourceId`, `SourceType`, `HoldingId`, `InstrumentId`, `AssetClass`, `AssetSubType`, `OwnershipSplitPct`, `ValuationId`, `ValuationMethod`, `ValuationAsOf`, `ValuationSource`, `TransactionId`, `TransactionDate`, `TransactionAmount`, `TransactionType`, `IncomeStreamType`, `IncomeAmount`, `CommitmentAmount`, `DocumentId`, `DocumentType`, `LiabilityId`, `LiabilityClass`, `ScheduleDate`, `ScheduledPrincipal`, `ScheduledInterest`, `ConsentScope`, `ConsentPurpose`, `ConsentExpiry`, `ConsentRevokedAt`.

### Required system-derived fields

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Derived | `HoldingCurrentValue` | Latest eligible valuation × ownership/quantity rules |
| Derived | `EntityAttributedHoldingValue` | Holding value × entity ownership split |
| Derived | `LiabilityOutstanding` | Outstanding balance from source/schedule |
| Derived | `EntityNetWorth` | Attributed assets minus attributed liabilities |
| Derived | `HouseholdNetWorth` | Deduplicated household assets minus liabilities |
| Rule/State | `VerificationLevel` | Level derived from source/evidence rules |
| Derived | `DataFreshnessAge` | Current time minus source/valuation as-of |
| Rule/State | `StalenessStatus` | Fresh/stale based on field/asset/source rule |
| Hidden | `CalculationVersion` | Version of formula/rule set |
| Hidden | `ProvenancePath` | Source → fact → valuation → metric lineage |
| Hidden | `AccessDecision` | Whether current actor may read/use a field |
| Hidden | `ActionEligibility` | Whether verification level permits downstream action |

**Engineering principle from the mock:** money should use integer minor units rather than floating-point storage.

---

## 20. `Settings.dc.html`

**Page purpose:** Identity, household roles, privacy, notifications, display, security, export/closure and commercial transparency.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `MemberSince` | Account membership date |
| Derived | `DaysSinceLastSettingsChange` | Current date minus last settings change |
| Source | `LegalName` | Verified legal name |
| Source | `DateOfBirth` | Verified DOB |
| Source | `PANMasked` | Masked tax identifier |
| Source | `TaxResidency` | Current tax residency |
| Source | `EmailMasked` | Masked contact |
| Source | `PhoneMasked` | Masked contact |
| Derived | `SubscriptionPaidToPlatform` | Subscription fees paid in period |
| Derived | `LenderRevenueToPlatform12M` | Fees platform earned from lenders due to user's activity |
| Derived | `MarketplaceRevenueToPlatform` | Marketplace fees earned from user's activity |
| Derived | `AdvisorPaymentsThroughPlatform` | User payments to advisors routed through platform |
| Derived | `TotalPlatformRevenueFromUserActivity` | Sum of applicable platform-earned revenue categories |
| Source | `HouseholdRole` | Owner/admin/guardian/etc. |
| Derived | `RoleAttributedValue` | Value of assets user owns/administers where shown |
| Source | `RoleStartDate` | Date role began |
| Rule/State | `ExportStatus` | Requested/processing/ready |
| Source | `ExportGeneratedAt` | Export timestamp |
| Rule/State | `AccountClosureStatus` | Active/closure requested/closed |
| Source | `NotificationPreferences` | User-selected notifications |
| Source | `DisplayPreferences` | Currency/format/display options |
| Source | `SecuritySettings` | MFA/session/security choices |
| Hidden | `TaxRuleContextVersion` | Rule context recalculated when tax residency changes |
| Hidden | `SettingsAuditLog` | Immutable record of material settings changes |

---

## 21. `Stamp collection.dc.html`

**Page purpose:** Marketplace detail and transaction workflow for a collectible asset.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `ListingAskingPrice` | Seller asking price |
| Source | `ListingDate` | Date listed |
| Derived | `DaysListed` | Current date minus listing date |
| Source | `CollectionPlateCount` | Number of plates |
| Source | `CollectionItemCount` | Number of stamps/items |
| Source | `GradedPlateCount` | Plates with grading |
| Derived | `GradedPlatePct` | `GradedPlateCount / PlateCount` |
| Source | `CatalogueReference` | Catalogue/edition used |
| Source | `SellerCompletedSalesCount` | Settled marketplace sales |
| Source | `SellerRatingCount` | Ratings from settled trades |
| Rule/State | `SellerKYCStatus` | KYC complete/incomplete |
| Source | `RequiredVerificationCheckCount` | Required checks for lot |
| Derived | `PassedVerificationCheckCount` | Checks passed |
| Derived | `VerificationCompletionPct` | Passed / required |
| Rule/State | `ListingVerificationStatus` | Verified/open/failed |
| Source | `OfferAmount` | Buyer offer |
| Derived | `OfferDiscountToAskingPct` | `(Asking - Offer) / Asking` |
| Source | `AgreedPrice` | Final negotiated consideration |
| Source | `BuyerFeePct` | Platform fee paid by buyer |
| Derived | `BuyerFeeAmount` | `AgreedPrice × BuyerFeePct` |
| Derived | `BuyerTotalCashRequired` | Agreed price + buyer fee + other required charges |
| Rule/State | `AgreementStatus` | Drafted/signed/etc. |
| Rule/State | `EscrowStatus` | Awaiting/funded/released/refunded |
| Source | `EscrowAmount` | Amount held |
| Rule/State | `SettlementStatus` | Pending/completed |
| Derived | `AcquiredAssetCostBasis` | Purchase consideration + capitalizable acquisition costs |
| Rule/State | `PortfolioBookingStatus` | Whether acquired asset is recorded in buyer ledger |
| Source | `AcquisitionValuationBasis` | Cost/other basis after purchase |

---

## 22. `Trends and news.dc.html`

**Page purpose:** Portfolio-relevant news filtered through actual holdings and exposures.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `ItemsScreenedCount` | Candidate news/trend items screened |
| Derived | `ItemsKeptCount` | Items passing relevance rules |
| Derived | `ItemsDroppedCount` | `Screened - Kept` |
| Derived | `NewsKeepRatePct` | `Kept / Screened` |
| Source | `ReadTimeMinutes` | Estimated reading time |
| Derived | `ItemCountByCategory` | Kept items by holdings/sectors/macro/not-held |
| Source | `NewsItemDate` | Publication/event date |
| Source | `NewsOutlet` | Named source |
| Source | `NewsItemKind` | Holding/sector/macro/etc. |
| Rule/State | `PortfolioRelevancePath` | Why item reaches user: holding → fund → sector etc. |
| Derived | `NewsAffectedExposureValue` | Portfolio value touched by item |
| Derived | `NewsAffectedExposurePct` | Affected exposure / relevant portfolio base |
| Derived | `SectorExposureValue` | Direct + look-through sector value |
| Derived | `SectorExposurePct` | Sector value / look-through base |
| Derived | `Sector3MReturn` | Sector return over three months |
| Hidden | `NewsRelevanceScore` | Internal ranking/filter score based on traceable exposure |
| Hidden | `NewsDeduplicationKey` | Prevent duplicate coverage of same event |
| Hidden | `NewsFreshnessScore` | Recency component used in ordering |
| Rule/State | `ZeroExposureWatchStatus` | Sector intentionally watched despite no holdings |

---

## 23. `User Flow.dc.html`

**Page purpose:** Product architecture/reference page describing how facts progress through verification and become usable across capabilities.

### Core system datapoints and derived states

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Rule/State | `VerificationLevel` | Level 1 self-declared; Level 2 documented; Level 3 verified; higher accepted/actionable state where defined |
| Source | `FactSource` | Origin of each stored fact |
| Source | `FactAsOf` | Time the fact is valid |
| Derived | `FactAge` | Current time minus fact as-of |
| Rule/State | `FactActionability` | Actions allowed at current verification level |
| Derived | `VerifiedWealthValue` | Wealth at/above required verification level |
| Derived | `VerifiedWealthPct` | Verified wealth / relevant total |
| Hidden | `CapabilityGate` | Whether a fact may be used in analysis/planning/credit/marketplace/resume/succession |
| Hidden | `VerificationUpgradePath` | Evidence/checks needed to move a fact to next level |
| Hidden | `CrossSurfaceConsistencyCheck` | Ensures same fact/metric is represented consistently on every screen |
| Hidden | `ProvenanceCompleteness` | Whether source, as-of and verification metadata are all present |

**Architecture rule:** verification is not merely a badge; it controls what downstream actions are permitted.

---

## 24. `User Story.dc.html`

**Page purpose:** Engineering build brief describing screen-by-screen behavior, system responsibilities and required states.

This page mostly defines **cross-product requirements** rather than unique consumer metrics. The following datapoints/states should exist globally:

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `StoredValueSource` | Source attached to every stored value |
| Source | `StoredValueAsOf` | As-of timestamp attached to every stored value |
| Rule/State | `StoredValueVerificationLevel` | Verification level attached to every stored value |
| Hidden | `ServerSideActionPermission` | What can be done with a value given its verification level |
| Derived | `ProvableWealthValue` | Wealth supported by sufficient evidence |
| Derived | `ProvableWealthPct` | Provable wealth / total relevant wealth |
| Hidden | `ScreenState` | Loading/empty/partial/stale/error/complete/actionable states |
| Hidden | `MissingDataState` | Explicit representation of absent rather than estimated data |
| Hidden | `StaleDataState` | Explicit representation of stale values |
| Hidden | `ConflictState` | Contradictory source/document/ownership data |
| Hidden | `ManualOverrideState` | User-entered correction with provenance |
| Hidden | `CalculationDependencyGraph` | Upstream facts used by each derived metric |
| Hidden | `AuditEvent` | Who/what changed a fact, rule, consent or value and when |
| Hidden | `AccessGrantEvaluation` | Field-level permission evaluation |
| Hidden | `HouseholdAttributionRule` | Prevents cross-member/joint double counting |
| Hidden | `ActionEligibilityReason` | Human-readable explanation when an action is blocked/allowed |

This page should be treated as a **test-case source** for the metric engine: every scenario described should map to deterministic data states and calculation outputs.

---

## 25. `Will.dc.html`

**Page purpose:** Estate-planning gap analysis: what an existing will says, what the person owns now, contradictions, decisions, drafting and keeping it current.

| Type | Metric / Datapoint | Definition / Formula |
|---|---|---|
| Source | `WillExecutionDate` | Date existing will was executed |
| Derived | `WillAgeYears` | Current date minus execution date |
| Source | `WillClauseCount` | Parsed substantive clauses |
| Source | `WillAssetReference` | Asset/property described in clause |
| Rule/State | `WillAssetStillOwned` | Whether referenced asset remains in estate |
| Derived | `EmptyBequestCount` | Clauses referring to assets no longer owned |
| Source | `CurrentEstateAssetCount` | Current assets potentially governed by estate plan |
| Derived | `WillCoveredAssetCount` | Current assets effectively addressed by will |
| Derived | `WillUncoveredAssetCount` | Current estate assets not effectively addressed |
| Derived | `GrossEstateValue` | Current value of estate assets |
| Derived | `WillCoveredEstateValue` | Value with effective disposition |
| Derived | `WillUncoveredEstateValue` | `GrossEstateValue - CoveredEstateValue` |
| Derived | `EstateCoveragePct` | `CoveredEstateValue / GrossEstateValue` |
| Derived | `AssetsAcquiredSinceWillCount` | Current assets acquired after will execution |
| Derived | `AssetsDisposedSinceWillCount` | Will-referenced assets disposed since execution |
| Rule/State | `NominationMismatchCount` | Count where nominee and intended beneficiary conflict |
| Derived | `NoNomineeAssetCount` | Estate assets lacking nomination where relevant |
| Derived | `NoNomineeValue` | Value of such assets |
| Rule/State | `BeneficiaryDecisionStatus` | Decision captured/pending per asset/class |
| Source | `BeneficiarySharePct` | Intended share |
| Derived | `BeneficiaryValue` | Covered estate value × share, where determinable |
| Rule/State | `GuardianDecisionStatus` | Guardian decision for minors where relevant |
| Rule/State | `ExecutorDecisionStatus` | Executor selected/pending |
| Source | `DraftingFee` | Advocate/professional fee |
| Source | `ExecutionCost` | Signing/registration/notary/etc. costs where applicable |
| Derived | `EstatePlanningCost` | Sum of will-planning professional/administrative costs |
| Derived | `EstatePlanningCostPct` | Cost / estate value |
| Source | `LastEstateReviewDate` | Last reconciliation of will against ledger |
| Derived | `DaysSinceEstateReview` | Current date minus review date |
| Hidden | `WillLedgerConflictCount` | Number of contradictions between will and current ledger |
| Hidden | `WillRefreshTriggerCount` | Material events since last review: acquisition, disposal, gift, death, relationship/nomination change |

---

# Cross-page core metrics

These should be implemented once in a central calculation layer and reused rather than independently recalculated by each screen.

| Core metric | Canonical definition | Major consumers |
|---|---|---|
| `TotalAssets` | Sum of attributable current asset values | Net worth, Household, Planning, Resume, Credit |
| `TotalLiabilities` | Sum of attributable outstanding liabilities | Net worth, Household, Resume, Credit |
| `NetWorth` | `TotalAssets - TotalLiabilities` | Net worth, Planning, Resume, Credit |
| `AssetCurrentValue` | Quantity × eligible price/valuation, with asset-specific rules | Almost all portfolio pages |
| `AttributedAssetValue` | Gross value × ownership share | Household, Resume, estate, credit |
| `VerificationLevel` | Evidence/source-based level | All surfaces |
| `VerifiedValue` | Value satisfying page/action verification threshold | Net worth, Connections, Credit, Resume |
| `VerifiedWealthPct` | Verified value / relevant total | Header, Connections, Net worth |
| `ValuationAgeDays` | Current time minus valuation as-of | Portfolio, Analysis, property, resume |
| `StalenessStatus` | Fresh/stale using source/asset-specific threshold | All analytical surfaces |
| `MonthlyInflows` | Sum of classified cash inflows | Portfolio, Household, Resume |
| `MonthlyOutflows` | Sum of classified cash outflows | Portfolio, Household |
| `DebtServiceRatio` | Required debt service / explicitly defined income base | Net worth, Resume, Credit |
| `LiquidityValue` | Assets realizable within specified time bucket | Resume, Credit, Planning |
| `DirectExposure` | Direct holding exposure | Attribution, Trends, Resume |
| `IndirectExposure` | Look-through exposure via funds/vehicles | Attribution, Trends, concentration alerts |
| `EffectiveExposure` | Direct + indirect exposure | Attribution, concentration |
| `PortfolioXIRR` | Money-weighted annualized return | Analysis, Ask where applicable |
| `PortfolioTWRR` | Time-weighted portfolio return | Analysis, Attribution |
| `GoalProjectedValue` | Future value under saved assumptions | Planning |
| `EstateValue` | Current value of assets included in estate | Will, Inheritance |
| `ConsentStatus` | Active/expired/revoked | Connections, Peers, sharing |
| `AccessDecision` | Field/action permission after evaluating grants/roles | Peers, Resume, Household, system-wide |
| `MetricAsOf` | As-of timestamp of output | Every financial output |
| `CalculationVersion` | Formula/rule version | Every derived metric |
| `ProvenancePath` | Sources and transformations supporting output | Ask, Resume, Credit, all auditable outputs |

---

# Recommended calculation conventions

## 1. Every derived metric should carry provenance

A derived value should not be stored/returned as only:

```json
{
  "metric": "NetWorth",
  "value": 64700000
}
```

Prefer an object conceptually equivalent to:

```json
{
  "metric": "NetWorth",
  "value_minor_units": 6470000000,
  "currency": "INR",
  "as_of": "2026-08-31T15:30:00+05:30",
  "calculation_version": "networth.v1",
  "verification_summary": {
    "verified_value_minor_units": 5260000000,
    "self_declared_value_minor_units": 1210000000
  },
  "is_partial": false,
  "source_ids": ["..."]
}
```

## 2. Do not silently interpolate missing financial history

Where a source/feed is down, retain the missing observation and mark the time series partial unless a specific metric methodology explicitly requires interpolation and discloses it.

## 3. Separate valuation from verification

An asset can be legally/documentarily verified while its **current value** is estimated. Model these separately:

- `OwnershipVerificationStatus`
- `ValuationVerificationStatus`
- `ValuationMethod`
- `ValuationAsOf`

## 4. Ownership must be applied before household aggregation

For jointly held assets:

```text
MemberAttributedValue = GrossAssetValue × MemberOwnershipPct
```

But household aggregation should count the gross asset only once.

## 5. Keep XIRR, TWRR and contribution separate

- **XIRR:** user's money-weighted experience.
- **TWRR:** performance of the portfolio independent of external-flow timing.
- **Contribution:** how much an asset/class added to total portfolio performance.

They are related but not interchangeable.

## 6. Use look-through exposure for concentration

```text
EffectiveIssuerExposure =
    DirectIssuerExposure
  + IndirectIssuerExposureThroughFunds
  + OtherLookThroughExposure
```

This is required for the mock's fund-overlap, sector-exposure and concentration statements.

## 7. Legal/tax rules must be versioned

For gift, inheritance, will, tax and transfer calculations, store at minimum:

```text
Jurisdiction
RuleEffectiveDate
RuleVersion
CalculationDate
Assumptions
ProfessionalReviewRequired (where applicable)
```

## 8. Separate facts from modeled outputs

Planning projections, property estimates, unlisted-company marks and scenario calculators should remain distinguishable from observed facts. Suggested flags:

```text
IsObserved
IsEstimated
IsModeled
IsSelfDeclared
IsVerified
```

## 9. Reconcile aggregate metrics

For any waterfall or attribution display:

```text
Sum(ComponentContributions) ≈ HeadlineChange
```

Any difference caused by rounding, FX, timing, residuals or unavailable data should be captured in an explicit reconciliation/residual field.

## 10. Use integer money storage

Store money in integer minor units with an explicit currency. Avoid binary floating-point for monetary values.

---

# Suggested engineering taxonomy

A practical metric service can group the above into eight reusable engines:

1. **Wealth & ownership** — assets, liabilities, net worth, member attribution.
2. **Valuation & verification** — price/valuation selection, freshness, evidence levels.
3. **Cash flow & debt** — income, expenses, surplus, amortization, debt service.
4. **Performance & attribution** — XIRR, TWRR, benchmarks, contribution.
5. **Exposure & concentration** — look-through, overlap, issuer/sector concentration.
6. **Planning & scenarios** — goals, future value, timing mismatches, calculators.
7. **Estate & transfer** — gifts, will coverage, inheritance, succession states.
8. **Consent, access & marketplace** — grants, disclosure, credit, listings, advisors.

This keeps page logic thin: pages consume canonical metrics instead of implementing their own financial calculations.

---

## Document status

- **Source reviewed:** 25 HTML mock files.
- **Output:** page-by-page metric/datapoint inventory.
- **Intended use:** GitHub specification for product, data and engineering review.
- **Recommended next artifact:** machine-readable metric registry (`metrics.yaml` or `metrics.json`) with IDs, formula definitions, dependencies, units, time grain, verification requirements and owning calculation engine.
