#!/usr/bin/env python3
"""
AWE Documents Downloader
Downloads all documents from www.awe.co.uk/document pages 1-20
"""

import os
import re
import time
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path

# Base URL for normalizing relative paths
BASE_URL = "https://www.awe.co.uk"

# Output directory
OUTPUT_DIR = "awe-docs"

# All document URLs collected from pages 1-20
DOCUMENT_URLS = [
    # Page 1
    "https://wp-content/uploads/2025/10/SUPPLIER-HANDBOOK_final_Oct-2025-1.pdf",
    "https://wp-content/uploads/2025/10/TCFD_AWE_YEAR3_MARCH2025-1.pdf",
    "https://wp-content/uploads/2025/09/GOV.UK-Board-Members-Declaration-of-Interests-2-8.pdf",
    "https://wp-content/uploads/2025/09/AWE-Engagement-Implementation-Statement-2025.pdf",
    "https://wp-content/uploads/2025/09/Tax-Strategy-2025.pdf",
    "https://wp-content/uploads/2025/09/AWE-Environment-and-Sustainability-Policy.pdf",
    "https://wp-content/uploads/2025/09/AWE-Safety-and-Health-Policy.pdf",
    "https://wp-content/uploads/2025/08/GOV.UK-Board-Members-Declaration-of-Interests-August-2025.pdf",
    "https://wp-content/uploads/2025/06/7128-v1.0-Environment-and-Sustainability-Policy-Statement-8.pdf",
    "https://wp-content/uploads/2025/07/111-LLC-minutes.pdf",
    "https://wp-content/uploads/2025/06/LLC_111_April2025_SlideDeck.pdf",
    "https://wp-content/uploads/2025/06/Code_of_Ethics_2025.pdf",
    "https://wp-content/uploads/2025/06/2025_AWE_EMERGENCY_TEXT_ALERT_FAQ.pdf",
    "https://wp-content/uploads/2025/05/20250601-ISO-9001_2015-BSI-Certificate.pdf",
    "https://wp-content/uploads/2025/05/20250601-ISO-14001_2015-BSI-Certificate.pdf",
    "https://wp-content/uploads/2025/05/7129-v-1.0-AWE-Safety-and-Health-Policy-statement.pdf",
    "https://wp-content/uploads/2023/03/6099-v1.3-AWE-Quality-Policy-statement_.pdf",
    "https://wp-content/uploads/2025/05/110-LLC-minutes-FINAL-1.pdf",
    "https://wp-content/uploads/2025/04/LLC-110-slide-deck.pdf",
    "https://wp-content/uploads/2025/04/Quality-Requirements-for-Suppliers-March-2025.pdf",

    # Page 2
    "/wp-content/uploads/2025/03/2024-5-Gender-Pay-Gap-Report.pdf",
    "/wp-content/uploads/2025/02/AWE-PLC-MSS-24-25.pdf",
    "/wp-content/uploads/2025/01/FOI-Request-Medical-Record-2.pdf",
    "/wp-content/uploads/2025/01/FOI-Request-LCI-118.pdf",
    "/wp-content/uploads/2025/01/FOI-Request-Medical-Record.pdf",
    "/wp-content/uploads/2025/01/FOI-Report-T16-93-Report.pdf",
    "/wp-content/uploads/2025/01/FOI-Request-Woomera.pdf",
    "/wp-content/uploads/2024/12/FOI-Request-Names-and-Job-Titles-AWE.pdf",
    "/wp-content/uploads/2024/12/FOI-Request-Medical-Record.pdf",
    "/wp-content/uploads/2024/12/FOI-Request-Army-and-Medical-Records.pdf",
    "/wp-content/uploads/2024/11/FOI-Request-AWE-Rebrand.pdf",
    "/wp-content/uploads/2024/11/FOI-Request-Bone-Sampling.pdf",
    "/wp-content/uploads/2024/11/FOI-Request-Call-of-contracts.pdf",
    "/wp-content/uploads/2024/11/FOI-Request-F-Med-Forms.pdf",
    "/wp-content/uploads/2024/11/FOI-Request-Mini-Merlin.pdf",
    "/wp-content/uploads/2024/11/FOI-Request-Roles-Grades-and-Average-AWE-Salaries.pdf",
    "/wp-content/uploads/2024/11/FOI-Request-Employment-Policies-and-Pay-Grades.pdf",
    "/wp-content/uploads/2024/10/2025-qualifications-matrix.pdf",
    "/wp-content/uploads/2024/10/AWE-Pension-Trustees-Ltd-–-Engagement-Policy-Implementation-Statement-ye-31-March-2024.pdf",

    # Page 3
    "https://wp-content/uploads/2024/10/AWE-Pension-Scheme-TCFD-Report-for-year-ended-31-March-2024.pdf",
    "https://wp-content/uploads/2024/09/Burghfield-infrastructure.pdf",
    "https://wp-content/uploads/2024/09/Project-Mensa-and-ATC.pdf",
    "https://wp-content/uploads/2024/09/Document-redactions.pdf",
    "https://wp-content/uploads/2024/09/Question-on-Archive-1.pdf",
    "https://wp-content/uploads/2024/08/A-summary-of-all-information-held-about-two-archives.pdf",
    "https://wp-content/uploads/2024/08/Burghfield-DEPZ.pdf",
    "https://wp-content/uploads/2024/08/Corporate-Strategy.pdf",
    "https://wp-content/uploads/2024/08/Film-and-TV-spending.pdf",
    "https://wp-content/uploads/2024/08/Follow-up-to-request-for-cloud-sampling-document.pdf",
    "https://wp-content/uploads/2024/08/Information-relating-to-Red-Beard.pdf",
    "https://wp-content/uploads/2024/08/JOWOG-details.pdf",
    "https://wp-content/uploads/2024/08/PA-pay-bands.pdf",
    "https://wp-content/uploads/2024/08/Summary-of-information-from-151-merlin-documents.pdf",
    "https://wp-content/uploads/2024/08/UK-Norway-exercise-photos.pdf",
    "https://wp-content/uploads/2024/08/Subject-Access-Request-Template-2018_O.docx",
    "https://wp-content/uploads/2024/07/Statement-of-Investment-Principles-June-2024.pdf",
    "https://wp-content/uploads/2024/07/Responsible-Investment-policy-June-2024.pdf",
    "https://wp-content/uploads/2024/07/5917-v1.2-CFSI-Policy.pdf",
    "https://wp-content/uploads/2024/06/SB8761-AWE_PS-SFS-online.pdf",

    # Page 4
    "https://www.awe.co.uk/wp-content/uploads/2024/06/Minutes-of-the-109th-AWE-Local-Liaison-Committee-Meeting-Final-.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/06/109th-LLC-Meeting-Presentation-Slides-Final.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/03/Merlin-database-Updated.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/03/AWE-Defence-Award_Application-Criteria-and-Nomination-Forms_Fillable-with-email-and-closing-date.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/03/Solar-Farm-correspondence.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/03/F-Med-form-query.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/03/Energy-recovery-centre-correspondence.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/03/Request-for-report.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/03/Merlin-database.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/03/LCI-Questions.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/03/Government-clearance.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/03/Confidentiality-clauses.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/03/Bullying-Harrassment.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/03/Secondary-question-about-Bioassy-samples.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/02/Nature-Recovery-Plan_A4_V5.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/01/Warick-university-statistics.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/01/Translation-interpretation-and-language-service-costs.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/01/LCI-on-150-documents.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/01/Information-on-Christmas-Island-tests.pdf",
    "https://www.awe.co.uk/wp-content/uploads/2024/01/Document-Request-CAFO-17-58-01.08.58.pdf",

    # Page 5
    "https://wp-content/uploads/2024/01/Code-of-Ethics-2022-Issue-6.1-May-2023.pdf",
    "https://wp-content/uploads/2024/01/Statement-of-Investment-Principles-approved-December-2023.pdf",
    "https://wp-content/uploads/2024/01/Minutes-of-the-108th-AWE-Local-Liaison-Committee-Meeting-Final.pdf",
    "https://wp-content/uploads/2024/01/108th-LLC-Meeting-Presentation-Slides-FINAL.pdf",
    "https://wp-content/uploads/2023/12/Question-on-AR-VR-technology.pdf",
    "https://wp-content/uploads/2023/12/Uranium-monitoring-jan-23-present.pdf",
    "https://wp-content/uploads/2023/12/Request-for-document.pdf",
    "https://wp-content/uploads/2023/12/Question-about-public-records-act.pdf",
    "https://wp-content/uploads/2023/12/ICT-Strategy.pdf",
    "https://wp-content/uploads/2023/12/information-on-UFO-UAP-AD-NHI.pdf",
    "https://wp-content/uploads/2023/12/Question-on-Operation-Pied-Piper.pdf",
    "https://wp-content/uploads/2023/11/37092-Codes-of-Conduct-2-UPDATED-2023_O-003.pdf",
    "https://wp-content/uploads/2023/10/AWE-Connect-Autumn-2023-web-ready-spreads.pdf",
    "https://wp-content/uploads/2023/10/Question-regarding-contractor-details.pdf",
    "https://wp-content/uploads/2023/10/Question-about-5-eyes-supply-chain-and-UAP.pdf",
    "https://wp-content/uploads/2023/10/Request-for-Op-buffalo-report.pdf",
    "https://wp-content/uploads/2023/10/Question-on-Off-site-emergency-plan.pdf",
    "https://wp-content/uploads/2023/10/AWE-plc-Annual-Report-and-Accounts-31-March-2023-signed.pdf",
    "https://wp-content/uploads/2023/10/AWE-Pension-Scheme-TCFD-report-2023.vf_.pdf",
    "https://wp-content/uploads/2023/10/AWE-Pension-Scheme-Final-EPIS-2023.pdf",

    # Page 6
    "https://wp-content/uploads/2023/09/ESG-Report_A4_FINAL1.pdf",
    "https://wp-content/uploads/2023/09/Further-Bioassy-52-67-question.pdf",
    "https://wp-content/uploads/2023/09/Call-off-contracts.pdf",
    "https://wp-content/uploads/2023/08/Waste-from-Maralinga.pdf",
    "https://wp-content/uploads/2023/08/Question-about-salesforce.pdf",
    "https://wp-content/uploads/2023/08/Question-about-project-sunshine.pdf",
    "https://wp-content/uploads/2023/08/Australian-Servicemen-Blood-examinations.pdf",
    "https://wp-content/uploads/2023/08/Australian-servicemen-blood-and-urine-tests.pdf",
    "https://wp-content/uploads/2023/08/30-day-outstanding-invoices.pdf",
    "https://wp-content/uploads/2023/08/Plutonium-samples-sellafield.pdf",
    "https://wp-content/uploads/2023/08/Corporate-estate-managing-maintenance.pdf",
    "https://wp-content/uploads/2023/08/DSUS-leaflet-v5.pdf",
    "https://wp-content/uploads/2023/07/Question-about-Procurement.pdf",
    "https://wp-content/uploads/2023/07/Follow-up-question-Bioassy-1952-1967.pdf",
    "https://wp-content/uploads/2023/07/Burghfield-developments.pdf",
    "https://wp-content/uploads/2023/07/Carbon-Management-Plan.pdf",
    "https://wp-content/uploads/2023/06/107th-LLC-Meeting-Presentation-Slides-FINAL-v2.pdf",
    "https://wp-content/uploads/2023/06/LLC-107-Minutes-Issued.pdf",
    "https://wp-content/uploads/2023/06/LLC-Members-June-2023-v3.pdf",

    # Page 7
    "https://wp-content/uploads/2023/05/Royal-fleet-auxiliaries-and-merchant-ships-file.pdf",
    "https://wp-content/uploads/2023/05/Cycle-to-work-scheme.pdf",
    "https://wp-content/uploads/2023/05/Question-about-Passengers-on-MS-Dunera.pdf",
    "https://wp-content/uploads/2023/05/Follow-up-question-about-Graduate-intake.pdf",
    "https://wp-content/uploads/2023/05/Follow-up-question-to-EIR2023-006-1.pdf",
    "https://wp-content/uploads/2023/05/Follow-up-question-to-FOI2023-007.pdf",
    "https://wp-content/uploads/2023/03/AWE_GPG-2022_FINAL.pdf",
    "https://wp-content/uploads/2023/02/Follow-up-to-request-about-urine-monitoring.pdf",
    "https://wp-content/uploads/2023/02/Question-about-blood-and-urine-monitoring.pdf",
    "https://wp-content/uploads/2023/02/Question-about-contacts-with-the-tobacco-industry.pdf",
    "https://wp-content/uploads/2023/02/Question-about-graduate-intake.pdf",
    "https://wp-content/uploads/2023/02/Question-about-Temporary-and-permanent-recruitment.pdf",
    "https://wp-content/uploads/2023/02/Request-for-1952-Blue-Danube-documentary.pdf",
    "https://wp-content/uploads/2023/02/Request-for-uranium-air-monitoring-data.pdf",
    "https://wp-content/uploads/2023/02/Question-about-Sputnik-report.pdf",
    "https://wp-content/uploads/2023/02/AWE-Benefits-Guide-Digital.pdf",
    "https://wp-content/uploads/2023/02/106th-LLC-Meeting-Presentation-Slides-FINAL.pdf",

    # Page 8
    "https://wp-content/uploads/2023/02/LLC-106-Minutes-Published.pdf",
    "https://wp-content/uploads/2023/01/AWE-Annual-Report-and-Accounts-2021-22-PUBLISHED-1.pdf",
    "https://wp-content/uploads/2023/01/Question-about-communications-regarding-Belgium-export-licences.pdf",
    "https://wp-content/uploads/2023/01/Question-about-Mental-health-policies.pdf",
    "https://wp-content/uploads/2023/01/Backscatter-Radar-reports-about-Orfordness.pdf",
    "https://wp-content/uploads/2023/01/Follow-up-question-on-Nigerian-correspondence.pdf",
    "https://wp-content/uploads/2023/01/Follow-up-to-Bioassy-samples-question.pdf",
    "https://wp-content/uploads/2023/01/Question-about-debrief-templates.pdf",
    "https://wp-content/uploads/2022/11/LLC-members-November-2022.pdf",
    "https://wp-content/uploads/2021/11/AWE-Tax-Strategy-FY23.pdf",
    "https://wp-content/uploads/2022/10/Diversity-and-Inclusion-metrics.pdf",
    "https://wp-content/uploads/2022/10/Question-about-Managed-print-etc.pdf",
    "https://wp-content/uploads/2022/10/Question-about-Nigerian-Meteorological-Service-correspondence.pdf",
    "https://wp-content/uploads/2022/10/Question-about-Sickness-Policies.pdf",
    "https://wp-content/uploads/2022/10/Question-about-Starlite.pdf",
    "https://wp-content/uploads/2022/10/Question-about-tunnels.pdf",
    "https://wp-content/uploads/2022/10/Question-about-Orfordness.pdf",
    "https://wp-content/uploads/2021/10/AWEPS-Engagement-Policy-Implementation-Statement-ye-31-March-2022_res.pdf",
    "https://wp-content/uploads/2022/08/Question-about-Costain-contract.pdf",

    # Page 9
    "https://awe.co.uk/wp-content/uploads/2022/08/Question-about-Grievance-Policies-and-Procedures.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/08/Question-about-Drone-sightings-in-January-22.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/08/Question-about-Misconduct.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/08/Question-about-Plutonium-from-Chalk-River.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/08/LLC-105-Minutes-Final.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/06/LLC-members-June-2022.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/05/LLC-members-May22.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/04/Question-about-pay-grades.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/04/Question-about-insurance.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/04/Question-about-Development-Management-Guidance-document.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/04/Question-about-Burghfield-pavilion-planning-application.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/04/LLC-104-Minutes-Issued-2.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/04/AWE-RB-Report-2021-April-6-FINAL.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/03/2186-AWE-Connect-Spring-2022-FINAL-singles.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/03/Follow-up-question-about-Stonewall.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/03/Question-about-health-charities.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/03/Test-Veteran-details.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/03/Deployment-of-emergency-flood-defences.pdf",
    "https://awe.co.uk/wp-content/uploads/2022/03/Malicious-emails.pdf",

    # Page 10
    "/wp-content/uploads/2022/03/Photos-of-2007-Burghfield-flood.pdf",
    "/wp-content/uploads/2022/03/Question-about-losses-and-special-payments.pdf",
    "/wp-content/uploads/2022/03/Question-about-Parental-leave-policies.pdf",
    "/wp-content/uploads/2022/02/LLC-103-Minutes-ISSUE.pdf",
    "/wp-content/uploads/2022/01/Question-about-human-experimentation-compressed.pdf",
    "/wp-content/uploads/2022/01/Question-about-Stonewall-1.pdf",
    "/wp-content/uploads/2022/01/Nigerian-Government-1959-visit-to-Harwell-1.pdf",
    "/wp-content/uploads/2022/01/Question-about-ONR-Ageing-assets-1.pdf",
    "/wp-content/uploads/2022/01/Software-question.pdf",
    "/wp-content/uploads/2022/01/NG-Bailey-Dismissial-1.pdf",
    "/wp-content/uploads/2022/01/Question-about-seismic-data-January-2001.pdf",
    "/wp-content/uploads/2022/01/Question-about-contracts-between-AWE-Plc-and-private-commercial-companies.pdf",
    "/wp-content/uploads/2022/01/Follow-up-question-about-IR35.pdf",
    "/wp-content/uploads/2021/11/Purchase-Order-Terms-June-2021.pdf",
    "/wp-content/uploads/2021/10/Gender-pay-gap-report2.pdf",
    "/wp-content/uploads/2021/09/Question-about-Charity-donations.pdf",
    "/wp-content/uploads/2021/09/Question-about-Pay-Review-2021.pdf",
    "/wp-content/uploads/2021/09/Question-about-cash-settlements-upon-employees-exit.pdf",
    "/wp-content/uploads/2021/09/Follow-up-question-on-Seismic-data-on-9-11.pdf",

    # Page 11
    "https://wp-content/uploads/2021/09/Request-for-AWRE-memo.pdf",
    "https://wp-content/uploads/2021/09/Question-about-Covid-Vaccines.pdf",
    "https://wp-content/uploads/2021/08/AWE_connect_final_Summer-2021.pdf",
    "https://wp-content/uploads/2021/08/LLC-102-Minutes-FINAL-1.pdf",
    "https://wp-content/uploads/2021/08/Question-about-UFOs-and-Drones.pdf",
    "https://wp-content/uploads/2021/08/LLC-members-Aug-2021.pdf",
    "https://wp-content/uploads/2021/08/FOI2021-002-Final-Response_anon.pdf",
    "https://wp-content/uploads/2021/08/Question-about-pylons-visible-from-the-M4.pdf",
    "https://wp-content/uploads/2021/07/20210630_AWE-FWD-Final_Secure_-v1.0.pdf",
    "https://wp-content/uploads/2021/06/00064-FOI-Request.pdf",
    "https://wp-content/uploads/2021/06/LLC-101-Minutes-ISSUED-v2.pdf",
    "https://wp-content/uploads/2021/04/Privacy-policy-03_O.pdf",
    "https://wp-content/uploads/2020/12/LLC-100-Minutes-FINAL.pdf",
    "https://wp-content/uploads/2020/12/AWE_connect_12pp_December-2020-spreads.pdf",
    "https://wp-content/uploads/2020/12/SCA-FAQs.pdf",
    "https://wp-content/uploads/2020/11/AWE-RB-Report-FINAL.pdf",
    "https://wp-content/uploads/2020/10/AWE-Pension-Trustees-Limited-Responsible-Investment-policy-Oct-20.pdf",
    "https://wp-content/uploads/2020/10/AWE-Pension-Scheme-Statement-of-Investment-Principles-September-2020-.pdf",
    "https://wp-content/uploads/2020/10/Future-Careers-brochure-FINAL.pdf",
    "https://wp-content/uploads/2020/08/20230112-WBC-REPPIR-booklet_A5-FINAL.pdf",

    # Page 12
    "https://wp-content/uploads/2020/08/LLC-99-Minutes-Issued.pdf",
    "https://wp-content/uploads/2020/06/LLC-TOR-Revised-Feb-2018_O.pdf",
    "https://wp-content/uploads/2020/06/LLC-98-Minutes-Issued.pdf",
    "https://wp-content/uploads/2020/06/BioDiversity_Action_plan-2020.pdf",
    "https://wp-content/uploads/2020/05/AWE_connect-A5-REPPIR_May-2020-singles-FINAL.pdf",
    "https://wp-content/uploads/2020/02/AWE-GenderPayGapReport_2020_FNL_25.02_optmised.pdf",
    "https://wp-content/uploads/2020/02/Supplier-Bulletin-Nov-19-final_O.pdf",
    "https://wp-content/uploads/2019/12/LLC-97-Minutes-Issue.pdf",
    "https://wp-content/uploads/2019/12/LLC-96-Minutes-ISSUE-1.pdf",
    "https://wp-content/uploads/2019/11/1976-AWE_connect_issue-22_12pp_November-2019-FINAL-spreads.pdf",
    "https://wp-content/uploads/2019/09/2019_August_Bulletin-final_O.pdf",
    "https://wp-content/uploads/2019/09/Supplier-Bulletin-May-19_O.pdf",
    "https://wp-content/uploads/2019/06/NEW-DISCOVERY-AUTUMN-WINTER-2018-19.pdf",
    "https://wp-content/uploads/2019/04/Apprentice-Brochure-2018.pdf",
    "https://wp-content/uploads/2019/04/AWE-Business-Strategy-to-2022.pdf",
    "https://wp-content/uploads/2019/04/LLC-94-Minutes-ISSUE.pdf",
    "https://wp-content/uploads/2019/04/LLC-93-Minutes-ISSUE.pdf",
    "https://wp-content/uploads/2019/04/LLC-92-Minutes-ISSUE.pdf",
    "https://wp-content/uploads/2019/04/LLC-95-Minutes-ISSUE.pdf",

    # Page 13
    "/wp-content/uploads/2019/03/Target-Diagnostics.pdf",
    "/wp-content/uploads/2019/03/AWE-GenderPayGapReport_Feb_2019.pdf",
    "/wp-content/uploads/2019/02/37050-Supply-chain-Brochure_Final-Nov-18.pdf",
    "/wp-content/uploads/2019/02/Supplier-Bulletin-Feb-19_O.pdf",
    "/wp-content/uploads/2018/05/Subject-Access-Request-Form-2018_O-5.docx",
    "/wp-content/uploads/2018/05/New-Discovery-edition-two-2018-low-res_O-5.pdf",
    "/wp-content/uploads/2018/05/REPPIR-2018-FINAL-PRINT-VERSION_APRIL-2018-5.pdf",
    "/wp-content/uploads/2018/05/Mays-Supplier-Bulletin_O-5.pdf",
    "/wp-content/uploads/2018/03/LLC-91-ISSUE_O-5.pdf",
    "/wp-content/uploads/2018/03/AWE-LLC-90-ISSUE_O-5.pdf",
    "/wp-content/uploads/2018/02/Februarys-Supplier-Bulletin_O-5.pdf",
    "/wp-content/uploads/2018/02/Novembers-Supplier-Bulletin_O-5.pdf",
    "/wp-content/uploads/2018/02/TOR-Members-Code-5.pdf",
    "/wp-content/uploads/2017/12/AWE_connect_issue-19_12pp_December-2017-Nov-22-p6-havanaman-5.pdf",

    # Page 14
    "/wp-content/uploads/2016/11/ESH-report-Apr-June-2016-FINAL-5.pdf",
    "/wp-content/uploads/2016/10/Physics-World-October-2016-5.pdf",
    "/wp-content/uploads/2016/10/LLC-86-Minutes-ISSUE-5.pdf",
    "/wp-content/uploads/2016/09/ESH-Qtr1-report-Jan-March-2016-5.pdf",
    "/wp-content/uploads/2016/08/LLC-85-Minutes-ISSUE-5.pdf",
    "/wp-content/uploads/2016/07/Travel-Plan-2015-5.pdf",
    "/wp-content/uploads/2016/05/AWE-Low-Risk-Low-Value-Terms-and-Conditions-PDF-5.pdf",
    "/wp-content/uploads/2016/05/Contract-Terms-and-Conditions-FULL-SET-PDF-5.pdf",
    "/wp-content/uploads/2016/05/Hoarty-HEDP-May-2016-5.pdf",
    "/wp-content/uploads/2016/05/AWE_connect_issue-18_May-2016_FINAL-PRINTED-VERSION1-5.pdf",
    "/wp-content/uploads/2016/05/LLC-84-Minutes-ISSUE-5.pdf",
    "/wp-content/uploads/2016/04/Brownjohn-JMW-et-al-Procs-ICE-Structures-and-buildings-Paper-1400133-2015-5.pdf",
    "/wp-content/uploads/2016/04/Orion-nature-article-5.pdf",
    "/wp-content/uploads/2016/04/OFL-Discovery-26_V9-FINAL-5.pdf",

    # Page 15
    "/wp-content/uploads/2016/03/ESH-report-Oct-Dec-2015-FINAL-5.pdf",
    "/wp-content/uploads/2016/01/LLC-83-Minutes-5.pdf",
    "/wp-content/uploads/2015/08/Light-Primary-School-5.pdf",
    "/wp-content/uploads/2015/08/Atoms-and-Bonds-5.pdf",
    "/wp-content/uploads/2015/08/Waves-5.pdf",
    "/wp-content/uploads/2015/08/Nuclear-Physics-5.pdf",
    "/wp-content/uploads/2015/08/Radioactivity-and-Nuclear-Power-5.pdf",
    "/wp-content/uploads/2015/08/Standard-Requirements-PDF-August-5.pdf",
    "/wp-content/uploads/2015/04/LLC-80-Minutes-22.04.15-5.pdf",

    # Page 16
    "https://awe.org.uk/wp-content/uploads/2015/08/AWE-Standard-Terms-and-Conditions-PDF-August-5.pdf",
    "https://awe.org.uk/wp-content/uploads/2014/10/Historical-documents-5.pdf",
    "https://awe.org.uk/wp-content/uploads/2014/09/Radiological-Monitoring-pdf-6.pdf",
    "https://awe.org.uk/wp-content/uploads/2014/10/LLC-Minutes-78-17th-September-2014-5.pdf",
    "https://awe.org.uk/wp-content/uploads/2014/10/LLC-meeting-77-Minutes-4-June-2014-6.pdf",
    "https://awe.org.uk/wp-content/uploads/2014/10/LLC-meeting-76-Minutes-26-March-2014-6.pdf",
    "https://awe.org.uk/wp-content/uploads/2014/10/LLC-meeting-75-Minutes-11-December-2013-6.pdf",
    "https://awe.org.uk/wp-content/uploads/2014/10/LLC-meeting-74-Minutes-18-September-13-6.pdf",
    "https://awe.org.uk/wp-content/uploads/2014/10/LLC-meeting-73-Minutes-12-June-13-6.pdf",
    "https://awe.org.uk/wp-content/uploads/2014/10/LLC-meeting-72-Minutes-13-March-13-6.pdf",
    "https://awe.org.uk/wp-content/uploads/2014/10/LLC-Meeting-71-5th-December-2012-6.pdf",
    "https://awe.org.uk/wp-content/uploads/2014/10/LLC-Meeting-70-19th-September-2012-6.pdf",

    # Page 17
    "/wp-content/uploads/2014/09/Connect_august-2014-6.pdf",
    "/wp-content/uploads/2014/09/Summary_Fire_Report_Findings-6.pdf",
    "/wp-content/uploads/2014/10/LLC-Meeting-69-20th-June-2012-6.pdf",
    "/wp-content/uploads/2014/10/LLC-Meeting-68-7th-March-2012-6.pdf",
    "/wp-content/uploads/2014/09/AWE-Connect-Summer-FINAL-spreads-2013-6.pdf",
    "/wp-content/uploads/2014/09/AWE-Connect-Winter-2012-FINAL-6.pdf",
    "/wp-content/uploads/2014/09/Discovery24September2013-6.pdf",
    "/wp-content/uploads/2014/09/Discovery23-July2012-6.pdf",
    "/wp-content/uploads/2014/09/68e180bAWE_Discovery_22-6.pdf",
    "/wp-content/uploads/2014/09/Discovery_21_December_2010-6.pdf",
    "/wp-content/uploads/2014/09/AWE-Connect-Summer-2012-FINAL-6.pdf",
    "/wp-content/uploads/2014/11/Burghfiled-Permit-5.pdf",
    "/wp-content/uploads/2014/09/AWE_Stress_Tests_Report-6.pdf",

    # Page 18
    "/wp-content/uploads/2014/11/Aldermaston-Permit-5.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No22-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No21-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No20-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No19-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No18-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No17-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No16-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No15-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No14-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No13-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No12-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No11-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No10-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No9-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No8-6.pdf",

    # Page 19
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No7-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No6-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No5-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No4-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No3-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No2-6.pdf",
    "/wp-content/uploads/2014/10/AWE-Orion-Fact-Sheet-No1-6.pdf",
    "/wp-content/uploads/2014/09/Connect_Winter_2011-6.pdf",
    "/wp-content/uploads/2014/09/Connect_Summer_2010-6.pdf",
    "/wp-content/uploads/2014/09/Connect-Winter-09-FINAL-6.pdf",
    "/wp-content/uploads/2014/09/Fire_Investigation_Main_Report-6.pdf",
    "/wp-content/uploads/2014/09/Connect_Summer_09-6.pdf",
    "/wp-content/uploads/2014/10/LLC-meetig-67-8th-December-20111-6.pdf",
    "/wp-content/uploads/2014/10/LLC-meeting-66-15th-September-2011-6.pdf",
    "/wp-content/uploads/2014/10/LLC-meeting-65-9th-June-2011-6.pdf",
    "/wp-content/uploads/2014/10/LLC-meeting-64-15th-March-2011-6.pdf",
    "/wp-content/uploads/2014/10/LLC-meeting-63-16th-December-2010-6.pdf",
    "/wp-content/uploads/2014/10/LLC-meeting-62-30th-September-2010-6.pdf",
    "/wp-content/uploads/2014/10/LLC-meeting-61-3rd-June-2010-6.pdf",

    # Page 20
    "/wp-content/uploads/2014/10/LLC-meeting-60-25th-March-2010-6.pdf",
]


def normalize_url(url):
    """
    Normalize URLs to full absolute URLs with https://www.awe.co.uk
    """
    # Remove leading/trailing whitespace
    url = url.strip()

    # Handle different URL patterns
    if url.startswith("https://www.awe.co.uk/"):
        return url
    elif url.startswith("https://awe.co.uk/"):
        return url.replace("https://awe.co.uk/", "https://www.awe.co.uk/")
    elif url.startswith("https://awe.org.uk/"):
        return url.replace("https://awe.org.uk/", "https://www.awe.co.uk/")
    elif url.startswith("https://wp-content/"):
        return url.replace("https://wp-content/", "https://www.awe.co.uk/wp-content/")
    elif url.startswith("/wp-content/"):
        return f"https://www.awe.co.uk{url}"
    elif url.startswith("wp-content/"):
        return f"https://www.awe.co.uk/{url}"
    else:
        return url


def get_filename_from_url(url):
    """
    Extract filename from URL
    """
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    return filename


def download_file(url, output_dir):
    """
    Download a single file
    """
    try:
        normalized_url = normalize_url(url)
        filename = get_filename_from_url(normalized_url)
        output_path = os.path.join(output_dir, filename)

        # Skip if file already exists
        if os.path.exists(output_path):
            print(f"✓ Skipped (exists): {filename}")
            return True

        # Download file
        response = requests.get(normalized_url, timeout=30, stream=True)
        response.raise_for_status()

        # Save file
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✓ Downloaded: {filename}")
        return True

    except Exception as e:
        print(f"✗ Failed: {filename} - {str(e)}")
        return False


def main():
    """
    Main function to download all documents
    """
    print(f"AWE Documents Downloader")
    print(f"=" * 60)

    # Create output directory
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Total documents to download: {len(DOCUMENT_URLS)}")
    print(f"=" * 60)
    print()

    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in DOCUMENT_URLS:
        normalized = normalize_url(url)
        if normalized not in seen:
            seen.add(normalized)
            unique_urls.append(url)

    print(f"Unique documents after deduplication: {len(unique_urls)}")
    print()

    # Download all files
    success_count = 0
    failed_count = 0

    for i, url in enumerate(unique_urls, 1):
        print(f"[{i}/{len(unique_urls)}] ", end="")
        if download_file(url, OUTPUT_DIR):
            success_count += 1
        else:
            failed_count += 1

        # Rate limiting - be polite to the server
        if i < len(unique_urls):
            time.sleep(0.5)

    # Summary
    print()
    print(f"=" * 60)
    print(f"Download complete!")
    print(f"Successful: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"Total: {len(unique_urls)}")
    print(f"Files saved to: {os.path.abspath(OUTPUT_DIR)}")
    print(f"=" * 60)


if __name__ == "__main__":
    main()
