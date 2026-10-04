export type Language = "en" | "hi" | "mr";

export interface Translations {
  // Navigation & Branding
  brandName: string;
  brandTagline: string;
  navAnalyze: string;
  navDocs: string;
  navAbout: string;

  // Language & Mode Selectors
  languageSelector: string;
  simpleModeLabel: string;
  simpleModeTooltip: string;

  // Analysis Modes
  tabUrl: string;
  tabMessage: string;
  tabScreenshot: string;
  urlPlaceholder: string;
  messagePlaceholder: string;
  screenshotUploadPrompt: string;
  screenshotUploadSub: string;
  analyzeButton: string;
  analyzingButton: string;
  loadDemoButton: string;
  fictionalDemoBadge: string;

  // Assessment & Overview
  overviewTitle: string;
  overallConcernTitle: string;
  levelLowConcern: string;
  levelModerateConcern: string;
  levelHighConcern: string;
  levelInsufficientEvidence: string;
  verifiedClaimsLabel: string;
  unverifiedClaimsLabel: string;
  contradictoryClaimsLabel: string;
  riskSignalsLabel: string;

  // Trust Chain
  trustChainTitle: string;
  trustChainSubtitle: string;
  trustChainVerified: string;
  trustChainUnverified: string;
  trustChainContradictory: string;
  trustChainUnknown: string;

  // Scam Journey
  scamJourneyTitle: string;
  scamJourneySubtitle: string;
  stageInitialContact: string;
  stageFinancialClaim: string;
  stageWebsite: string;
  stageCommunication: string;
  stageDepositRequest: string;
  stageWithdrawalIssue: string;
  stageObserved: string;
  stageSuspected: string;
  stageNotObserved: string;

  // Safe Response (Phase 9)
  safeResponseTitle: string;
  safeResponseSubtitle: string;
  actionStateTitle: string;
  actionStateSafe: string;
  actionStatePause: string;
  actionStateCaution: string;
  actionStatePostIncident: string;
  actionStateInsufficient: string;

  // Actions
  actionPause: string;
  actionVerify: string;
  actionDoNotSendMoney: string;
  actionDoNotShareCreds: string;
  actionDoNotInstallApp: string;
  actionPreserveEvidence: string;
  actionContactBank: string;
  actionReport: string;
  actionMonitor: string;

  // User Interactive Question
  userQuestionMoney: string;
  userQuestionCreds: string;
  optionYes: string;
  optionNo: string;
  optionNotSure: string;

  // Recovery Guidance
  recoveryTitle: string;
  recoverySubtitle: string;
  recoveryStopMoneyTitle: string;
  recoveryPreserveTitle: string;
  recoveryContactBankTitle: string;
  recoveryReportTitle: string;
  recoveryDeviceSecurityTitle: string;

  // Incident Timeline
  timelineTitle: string;
  timelineSubtitle: string;

  // Trust Breakpoint / Where Should I Stop?
  trustBreakpointTitle: string;
  trustBreakpointBadge: string;
  trustBreakpointStopPrefix: string;
  trustBreakpointStopGeneric: string;
  trustBreakpointWhy: string;
  trustBreakpointSupportingSignals: string;
  trustBreakpointViewEvidence: string;
  trustBreakpointRecommendedStop: string;
  trustBreakpointNoExplicitPayment: string;
  trustBreakpointNoExplicitPaymentDesc: string;
  trustBreakpointInsufficientEvidence: string;
  trustBreakpointSimpleModeExplanation: string;

  // Claim Spotlight
  claimSpotlightTitle: string;
  claimSpotlightSource: string;
  claimSpotlightObservation: string;
  claimSpotlightVerification: string;
  claimSpotlightWhyItMatters: string;
  claimSpotlightViewEvidence: string;
  claimSpotlightSelectPrompt: string;

  // Disclaimers & Notices
  disclaimerText: string;
  recoveryDisclaimerText: string;
  ocrNoticeTitle: string;
  plainLanguageActiveNotice: string;

  // Production Error Handlers
  errorBackendUnavailable: string;
  errorTimeout: string;
  errorPayloadTooLarge: string;
  errorUnsupportedMedia: string;
  errorRateLimited: string;
  errorGenericAnalysis: string;
}


export const translations: Record<Language, Translations> = {
  en: {
    brandName: "RakshaScan",
    brandTagline: "Authoritative Financial Trust Verification",
    navAnalyze: "Verify Counterparty",
    navDocs: "Registry Coverage",
    navAbout: "Safety Architecture",

    languageSelector: "Language",
    simpleModeLabel: "Simple explanation",
    simpleModeTooltip: "Displays simplified plain-language explanations for all safety assessments",

    tabUrl: "Website URL",
    tabMessage: "Copied Message",
    tabScreenshot: "Screenshot OCR",
    urlPlaceholder: "https://example-financial-advisory.com",
    messagePlaceholder: "Paste financial message, SMS, WhatsApp offer, or investment pitch here...",
    screenshotUploadPrompt: "Drop financial promo, chat screenshot, or app banner",
    screenshotUploadSub: "PNG, JPG, WEBP up to 10MB • Processed strictly with local OCR",
    analyzeButton: "Verify Authorizations",
    analyzingButton: "Inspecting Registries...",
    loadDemoButton: "Load Fictional Demo",
    fictionalDemoBadge: "FICTIONAL DEMONSTRATION INPUT",

    overviewTitle: "Assessment Synthesis",
    overallConcernTitle: "Concern Level",
    levelLowConcern: "Low Observed Concern",
    levelModerateConcern: "Moderate Concern — Pause & Verify",
    levelHighConcern: "High Concern — Safety Action Required",
    levelInsufficientEvidence: "Insufficient Evidence to Conclude",
    verifiedClaimsLabel: "Authoritatively Verified",
    unverifiedClaimsLabel: "Unverified / Unconfirmed",
    contradictoryClaimsLabel: "Contradictory to Official Record",
    riskSignalsLabel: "Detected Risk Patterns",

    trustChainTitle: "Financial Trust Chain",
    trustChainSubtitle: "Graph of entity claims, claimed registrations, and observed communication channels",
    trustChainVerified: "Verified Authentic",
    trustChainUnverified: "Uncorroborated",
    trustChainContradictory: "Contradictory Record",
    trustChainUnknown: "Status Unknown",

    scamJourneyTitle: "Scam Journey Reconstruction",
    scamJourneySubtitle: "Reconstructed sequence of observed interactions and payment requests",
    stageInitialContact: "Initial Contact",
    stageFinancialClaim: "Financial Claim",
    stageWebsite: "Website Landing",
    stageCommunication: "Communication Channel",
    stageDepositRequest: "Deposit Request",
    stageWithdrawalIssue: "Withdrawal Friction",
    stageObserved: "Observed in Content",
    stageSuspected: "Suspected Pattern",
    stageNotObserved: "Not Observed",

    safeResponseTitle: "What should you do now?",
    safeResponseSubtitle: "Evidence-aware safe response actions based on observed indicators",
    actionStateTitle: "Recommended Action State",
    actionStateSafe: "Safe to Continue with Standard Verification",
    actionStatePause: "Pause and Verify Before Transacting",
    actionStateCaution: "High Caution — Protective Action Recommended",
    actionStatePostIncident: "Post-Incident Recovery Mode Active",
    actionStateInsufficient: "Insufficient Information to Conclude",

    actionPause: "Pause Before Transferring Any Funds",
    actionVerify: "Verify Credentials on Official Portals",
    actionDoNotSendMoney: "Do Not Send Additional Funds to Unlock Balances",
    actionDoNotShareCreds: "Never Share Passwords, OTPs, PINs, or CVV",
    actionDoNotInstallApp: "Do Not Install Remote Desktop Apps or Unknown APKs",
    actionPreserveEvidence: "Preserve All Chat Records and Transaction Reference IDs",
    actionContactBank: "Contact Your Bank or Payment App Immediately",
    actionReport: "Report via Official Jurisdictional Channels",
    actionMonitor: "Monitor Account Statements Routinely",

    userQuestionMoney: "Have you already transferred money to this counterparty?",
    userQuestionCreds: "Have you shared passwords, OTPs, or banking PINs?",
    optionYes: "Yes",
    optionNo: "No",
    optionNotSure: "Not sure",

    recoveryTitle: "Protective Recovery Guidance",
    recoverySubtitle: "Steps to minimize exposure if money or credentials were transferred",
    recoveryStopMoneyTitle: "1. Stop Any Further Money Transfers",
    recoveryPreserveTitle: "2. Preserve Evidence & Reference Numbers",
    recoveryContactBankTitle: "3. Notify Your Bank or Payment Provider Immediately",
    recoveryReportTitle: "4. Lodge an Official Police or Cyber Crime Report",
    recoveryDeviceSecurityTitle: "5. Secure Affected Accounts and Devices",

    timelineTitle: "Observed Incident Timeline",
    timelineSubtitle: "Milestones established strictly from observed submission artifacts and user declarations",

    trustBreakpointTitle: "Where should you stop?",
    trustBreakpointBadge: "TRUST BREAKPOINT",
    trustBreakpointStopPrefix: "STOP BEFORE SENDING",
    trustBreakpointStopGeneric: "STOP BEFORE SENDING MONEY",
    trustBreakpointWhy: "WHY?",
    trustBreakpointSupportingSignals: "Supporting signals",
    trustBreakpointViewEvidence: "View supporting evidence",
    trustBreakpointRecommendedStop: "Recommended stop point",
    trustBreakpointNoExplicitPayment: "NO EXPLICIT PAYMENT STEP DETECTED",
    trustBreakpointNoExplicitPaymentDesc: "RakshaScan identified risk signals, but the submitted content does not contain enough evidence to identify a specific financial transaction stop point.",
    trustBreakpointInsufficientEvidence: "INSUFFICIENT EVIDENCE FOR STOP POINT",
    trustBreakpointSimpleModeExplanation: "RakshaScan found the point where you are being asked to send money. This is where you should stop and verify first.",

    claimSpotlightTitle: "Claim → Evidence Spotlight",
    claimSpotlightSource: "SOURCE",
    claimSpotlightObservation: "OBSERVATION",
    claimSpotlightVerification: "VERIFICATION STATUS",
    claimSpotlightWhyItMatters: "WHY IT MATTERS",
    claimSpotlightViewEvidence: "View evidence",
    claimSpotlightSelectPrompt: "Click any claim to inspect its underlying verification status and evidence.",

    disclaimerText: "RakshaScan provides safety and verification guidance. It does not provide investment advice, guarantee financial outcomes, or determine legal liability.",
    recoveryDisclaimerText: "If money or credentials may already have been exposed, immediately contact your financial provider through verified channels and preserve evidence.",
    ocrNoticeTitle: "Local OCR Notice",
    plainLanguageActiveNotice: "Simple explanation mode is enabled.",

    errorBackendUnavailable: "Cannot connect to the RakshaScan server. Please ensure the backend is running.",
    errorTimeout: "The analysis request timed out. Please try again.",
    errorPayloadTooLarge: "The submitted input or image is too large. Please submit a smaller payload.",
    errorUnsupportedMedia: "Unsupported file format. Please upload a PNG, JPEG, or WEBP image.",
    errorRateLimited: "Too many requests. Please wait a moment before trying again.",
    errorGenericAnalysis: "RakshaScan could not complete the analysis right now. Please try again.",
  },


  hi: {
    brandName: "रक्षास्कैन (RakshaScan)",
    brandTagline: "प्रामाणिक वित्तीय विश्वास एवं सुरक्षा सत्यापन",
    navAnalyze: "सत्यापन करें",
    navDocs: "नियामक रजिस्ट्री",
    navAbout: "सुरक्षा रूपरेखा",

    languageSelector: "भाषा (Language)",
    simpleModeLabel: "सरल भाषा स्पष्टीकरण",
    simpleModeTooltip: "जटिल वित्तीय नियमों को समझने के लिए सरल एवं स्पष्ट भाषा में विवरण",

    tabUrl: "वेबसाइट लिंक (URL)",
    tabMessage: "कॉपी किया गया संदेश",
    tabScreenshot: "स्क्रीनशॉट (OCR)",
    urlPlaceholder: "https://example-financial-advisory.com",
    messagePlaceholder: "वित्तीय संदेश, एसएमएस, व्हाट्सएप ऑफर या निवेश का दावा यहाँ पेस्ट करें...",
    screenshotUploadPrompt: "प्रमोशनल कार्ड, चैट स्क्रीनशॉट या विज्ञापन छवि यहाँ डालें",
    screenshotUploadSub: "PNG, JPG, WEBP अधिकतम 10MB • केवल आपके डिवाइस पर स्थानीय रूप से विश्लेषित",
    analyzeButton: "सत्यापन प्रारंभ करें",
    analyzingButton: "रजिस्ट्री की जाँच जारी...",
    loadDemoButton: "काल्पनिक डेमो लोड करें",
    fictionalDemoBadge: "काल्पनिक प्रदर्शन इनपुट (डेमो)",

    overviewTitle: "सत्यापन निष्कर्ष",
    overallConcernTitle: "सुरक्षा चिंता स्तर",
    levelLowConcern: "कम जोखिम — कोई चिंताजनक संकेत नहीं",
    levelModerateConcern: "मध्यम चिंता — रुकें और पुष्टि करें",
    levelHighConcern: "अत्यधिक चिंता — तत्काल सुरक्षा कदम आवश्यक",
    levelInsufficientEvidence: "निष्कर्ष के लिए अपर्याप्त साक्ष्य",
    verifiedClaimsLabel: "आधिकारिक रूप से सत्यापित",
    unverifiedClaimsLabel: "अपुष्ट / असत्यापित दावे",
    contradictoryClaimsLabel: "आधिकारिक रिकॉर्ड के विपरीत",
    riskSignalsLabel: "पाए गए जोखिम पैटर्न",

    trustChainTitle: "वित्तीय विश्वास श्रृंखला (Trust Chain)",
    trustChainSubtitle: "संस्था के दावों, पंजीकरणों और संपर्क माध्यमों का सत्यापन संबंध",
    trustChainVerified: "सत्यापित प्रामाणिक",
    trustChainUnverified: "स्वतंत्र रूप से अपुष्ट",
    trustChainContradictory: "असंगत रिकॉर्ड",
    trustChainUnknown: "स्थिति अज्ञात",

    scamJourneyTitle: "अनुक्रमिक पैटर्न विश्लेषण (Scam Journey)",
    scamJourneySubtitle: "संदेश से लेकर भुगतान अनुरोध तक की पहचानी गई चरणबद्ध प्रक्रिया",
    stageInitialContact: "प्रारंभिक संपर्क",
    stageFinancialClaim: "वित्तीय दावा",
    stageWebsite: "वेबसाइट आगमन",
    stageCommunication: "बातचीत का माध्यम",
    stageDepositRequest: "राशि जमा करने की मांग",
    stageWithdrawalIssue: "निकासी में रुकावट या शुल्क मांग",
    stageObserved: "साक्ष्य में उपस्थित",
    stageSuspected: "संभावित पैटर्न",
    stageNotObserved: "उपस्थित नहीं",

    safeResponseTitle: "अब आपको क्या करना चाहिए?",
    safeResponseSubtitle: "मिले हुए साक्ष्यों के आधार पर सुरक्षित कदम",
    actionStateTitle: "अनुशंसित कार्रवाई स्थिति",
    actionStateSafe: "मानक सत्यापन के साथ आगे बढ़ना सुरक्षित",
    actionStatePause: "लेनदेन से पहले रुकें और जांच करें",
    actionStateCaution: "उच्च सावधानी — सुरक्षात्मक कार्रवाई आवश्यक",
    actionStatePostIncident: "पुनर्प्राप्ति एवं सुरक्षा मोड सक्रिय",
    actionStateInsufficient: "निष्कर्ष के लिए जानकारी अपर्याप्त है",

    actionPause: "कोई भी राशि भेजने से पहले रुकें",
    actionVerify: "आधिकारिक सरकारी पोर्टल पर पंजीकरण संख्या जांचें",
    actionDoNotSendMoney: "अतिरिक्त शुल्क या निकासी के नाम पर पैसे न भेजें",
    actionDoNotShareCreds: "पासवर्ड, ओटीपी, पिन या सीवीवी कभी साझा न करें",
    actionDoNotInstallApp: "अज्ञात एपीके या रिमोट डेस्कटॉप ऐप इंस्टॉल न करें",
    actionPreserveEvidence: "स्क्रीनशॉट, चैट और बैंक रेफरेंस नंबर सुरक्षित रखें",
    actionContactBank: "अपने बैंक या पेमेंट ऐप से तुरंत संपर्क करें",
    actionReport: "आधिकारिक साइबर सेल या सरकारी पोर्टल पर रिपोर्ट करें",
    actionMonitor: "खाते के लेन-देन पर नियमित निगरानी रखें",

    userQuestionMoney: "क्या आपने पहले ही इस पक्ष को पैसे भेजे हैं?",
    userQuestionCreds: "क्या आपने पासवर्ड, ओटीपी या यूपीआई पिन साझा किया है?",
    optionYes: "हाँ",
    optionNo: "नहीं",
    optionNotSure: "निश्चित नहीं",

    recoveryTitle: "सुरक्षा एवं पुनर्प्राप्ति मार्गदर्शन",
    recoverySubtitle: "यदि राशि या विवरण साझा हुआ है तो नुकसान सीमित करने के कदम",
    recoveryStopMoneyTitle: "1. किसी भी तरह का अतिरिक्त भुगतान रोकें",
    recoveryPreserveTitle: "2. सबूत और रेफरेंस नंबर सहेजें",
    recoveryContactBankTitle: "3. तुरंत अपने बैंक के आधिकारिक नंबर पर संपर्क करें",
    recoveryReportTitle: "4. राष्ट्रीय साइबर अपराध पोर्टल (cybercrime.gov.in / 1930) पर रिपोर्ट करें",
    recoveryDeviceSecurityTitle: "5. खाते का पासवर्ड व यूपीआई पिन बदलें",

    timelineTitle: "घटनाक्रम की समयरेखा",
    timelineSubtitle: "उपलब्ध साक्ष्य और आपके विवरण के आधार पर बना क्रम",

    trustBreakpointTitle: "आपको कहाँ रुकना चाहिए?",
    trustBreakpointBadge: "विश्वास खंड बिंदु (TRUST BREAKPOINT)",
    trustBreakpointStopPrefix: "पैसे भेजने से पहले रुकें",
    trustBreakpointStopGeneric: "पैसे भेजने से पहले रुकें",
    trustBreakpointWhy: "क्यों?",
    trustBreakpointSupportingSignals: "संबंधित जोखिम संकेत",
    trustBreakpointViewEvidence: "संबंधित साक्ष्य देखें",
    trustBreakpointRecommendedStop: "रुकने की अनुशंसित जगह",
    trustBreakpointNoExplicitPayment: "पैसे भेजने का कोई प्रत्यक्ष कदम नहीं मिला",
    trustBreakpointNoExplicitPaymentDesc: "रक्षास्कैन ने जोखिम संकेत पाए हैं, लेकिन प्रस्तुत सामग्री में पैसे भेजने या ट्रांसफर करने का कोई प्रत्यक्ष वित्तीय कदम नहीं मिला।",
    trustBreakpointInsufficientEvidence: "रुकने का बिंदु तय करने के लिए अपर्याप्त साक्ष्य",
    trustBreakpointSimpleModeExplanation: "रक्षास्कैन ने वह बिंदु पहचाना है जहाँ आपसे पैसे भेजने के लिए कहा जा रहा है। पैसे भेजने से पहले यहीं रुकें और पहले पुष्टि करें।",

    claimSpotlightTitle: "दावा → साक्ष्य विस्तार (Spotlight)",
    claimSpotlightSource: "स्रोत",
    claimSpotlightObservation: "निरीक्षण",
    claimSpotlightVerification: "सत्यापन स्थिति",
    claimSpotlightWhyItMatters: "यह क्यों महत्वपूर्ण है?",
    claimSpotlightViewEvidence: "साक्ष्य देखें",
    claimSpotlightSelectPrompt: "किसी भी दावे पर क्लिक करके उसका सत्यापन और साक्ष्य देखें।",

    disclaimerText: "रक्षास्कैन केवल सुरक्षा और सत्यापन मार्गदर्शन प्रदान करता है। यह कोई कानूनी फैसला या निवेश सलाह नहीं देता है।",
    recoveryDisclaimerText: "यदि पैसे या क्रेडेंशियल्स साझा हुए हैं, तो तुरंत आधिकारिक बैंक चैनल का उपयोग करें और साक्ष्य सुरक्षित रखें।",
    ocrNoticeTitle: "स्थानीय ओसीआर सूचना",
    plainLanguageActiveNotice: "सरल भाषा मोड सक्रिय है।",

    errorBackendUnavailable: "रक्षास्कैन सर्वर से संपर्क नहीं हो सका। कृपया जांचें कि बैकएंड चालू है।",
    errorTimeout: "विश्लेषण अनुरोध का समय समाप्त हो गया। कृपया पुनः प्रयास करें।",
    errorPayloadTooLarge: "प्रस्तुत इनपुट या चित्र बहुत बड़ा है। कृपया छोटा पेलोड सबमिट करें।",
    errorUnsupportedMedia: "असमर्थित फ़ाइल प्रारूप। कृपया PNG, JPEG, या WEBP छवि अपलोड करें।",
    errorRateLimited: "बहुत अधिक अनुरोध। कृपया पुनः प्रयास करने से पहले कुछ क्षण प्रतीक्षा करें।",
    errorGenericAnalysis: "रक्षास्कैन अभी विश्लेषण पूरा नहीं कर सका। कृपया पुनः प्रयास करें।",
  },

  mr: {
    brandName: "रक्षास्कॅन (RakshaScan)",
    brandTagline: "विश्वासार्ह आर्थिक सुरक्षा पडताळणी",
    navAnalyze: "पडताळणी करा",
    navDocs: "अधिकृत नोंदणी",
    navAbout: "सुरक्षा चौकट",

    languageSelector: "भाषा (Language)",
    simpleModeLabel: "सोप्या भाषेतील स्पष्टीकरण",
    simpleModeTooltip: "सामान्य नागरिकांसाठी सोप्या भाषेत माहिती समजून घेण्यासाठी",

    tabUrl: "संकेतस्थळ (URL)",
    tabMessage: "मेसेज मजकूर",
    tabScreenshot: "स्क्रीनशॉट (OCR)",
    urlPlaceholder: "https://example-financial-advisory.com",
    messagePlaceholder: "आर्थिक मेसेज, एसएमएस, व्हॉट्सअ‍ॅपवरील ऑफर किंवा गुंतवणुकीचा मजकूर येथे पेस्ट करा...",
    screenshotUploadPrompt: "प्रमोशनल बॅनर किंवा चॅटचा स्क्रीनशॉट येथे टाका",
    screenshotUploadSub: "PNG, JPG, WEBP जास्तीत जास्त 10MB • डेटा केवळ आपल्याच डिव्हाइसवर तपासला जातो",
    analyzeButton: "पडताळणी सुरू करा",
    analyzingButton: "नोंदणी तपासत आहे...",
    loadDemoButton: "काल्पनिक नमुना लोड करा",
    fictionalDemoBadge: "काल्पनिक प्रात्यक्षिक माहिती (डेमो)",

    overviewTitle: "पडताळणी निष्कर्ष",
    overallConcernTitle: "सुरक्षा पातळी",
    levelLowConcern: "कमी धोका — कोणतेही संशयास्पद संकेत नाहीत",
    levelModerateConcern: "मध्यम काळजी — थांबा आणि खात्री करा",
    levelHighConcern: "उच्च धोका — तातडीने सावधगिरी बाळगा",
    levelInsufficientEvidence: "निष्कर्ष काढण्यासाठी पुरावे अपुरे आहेत",
    verifiedClaimsLabel: "अधिकृतरीत्या सत्यापित",
    unverifiedClaimsLabel: "अपुष्ट / असत्यापित दावे",
    contradictoryClaimsLabel: "अधिकृत नोंदीशी विसंगत",
    riskSignalsLabel: "आढळलेले संशयास्पद पॅटर्न",

    trustChainTitle: "आर्थिक विश्वास साखळी (Trust Chain)",
    trustChainSubtitle: "संस्थेचे दावे, नोंदणी क्रमांक आणि संपर्क माध्यमांचे पडताळणी संबंध",
    trustChainVerified: "सत्यापित अधिकृत",
    trustChainUnverified: "स्वतंत्र पुरावा उपलब्ध नाही",
    trustChainContradictory: "नोंदीशी विसंगत",
    trustChainUnknown: "स्थिती अज्ञात",

    scamJourneyTitle: "संभाव्य फसवणूक टप्पे (Scam Journey)",
    scamJourneySubtitle: "संदेशापासून ते पैसे मागण्यापर्यंत आढळलेले टप्पे",
    stageInitialContact: "पहिला संपर्क",
    stageFinancialClaim: "आर्थिक परताव्याचा दावा",
    stageWebsite: "संकेतस्थळाला भेट",
    stageCommunication: "संभाषणाचे माध्यम",
    stageDepositRequest: "पैसे भरण्याची मागणी",
    stageWithdrawalIssue: "पैसे काढताना अडचण / अतिरिक्त शुल्क",
    stageObserved: "मजकुरात आढळले",
    stageSuspected: "संशयित पॅटर्न",
    stageNotObserved: "आढळले नाही",

    safeResponseTitle: "आता आपण काय करावे?",
    safeResponseSubtitle: "सापडलेल्या पुराव्यांच्या आधारे सुरक्षित पुढील पावले",
    actionStateTitle: "सल्ला दिलेली कृती स्थिती",
    actionStateSafe: "साध्या खात्रीसह पुढे जाणे सुरक्षित",
    actionStatePause: "कोणताही व्यवहार करण्यापूर्वी थांबा आणि खात्री करा",
    actionStateCaution: "अतिदक्षता — तात्काळ बचावात्मक पावले उचला",
    actionStatePostIncident: "नुकसान निवारण मार्गदर्शन सक्रिय",
    actionStateInsufficient: "निर्णय घेण्यासाठी माहिती अपुरी आहे",

    actionPause: "कोणतेही पैसे पाठवण्यापूर्वी थांबा",
    actionVerify: "अधिकृत सरकारी पोर्टलवर नोंदणी क्रमांक तपासा",
    actionDoNotSendMoney: "पैसे सोडवून घेण्यासाठी अतिरिक्त शुल्क भरू नका",
    actionDoNotShareCreds: "पासवर्ड, ओटीपी, पिन किंवा सीव्हीव्ही कधीही देऊ नका",
    actionDoNotInstallApp: "अनोळखी अ‍ॅप किंवा रिमोट स्क्रीन शेअरिंग अ‍ॅप टाळा",
    actionPreserveEvidence: "चॅटचे स्क्रीनशॉट आणि बँक व्यवहाराचे संदर्भ क्रमांक जपून ठेवा",
    actionContactBank: "आपल्या बँकेशी किंवा पेमेंट अ‍ॅपशी त्वरित संपर्क साधा",
    actionReport: "अधिकृत सायबर पोर्टलवर तक्रार नोंदवा",
    actionMonitor: "आपल्या बँक खात्यावर नियमित लक्ष ठेवा",

    userQuestionMoney: "आपण या आधीच या व्यक्तीला किंवा संस्थेला पैसे पाठवले आहेत का?",
    userQuestionCreds: "आपण आपले पासवर्ड किंवा ओटीपी शेअर केला आहे का?",
    optionYes: "होय",
    optionNo: "नाही",
    optionNotSure: "नक्की सांगता येत नाही",

    recoveryTitle: "सुरक्षितता व भरपाई मार्गदर्शन",
    recoverySubtitle: "पैसे किंवा माहिती दिली असल्यास संभाव्य नुकसान टाळण्यासाठी पावले",
    recoveryStopMoneyTitle: "1. पुढील कोणतेही पैसे पाठवणे तात्काळ थांबवा",
    recoveryPreserveTitle: "2. चॅटचे स्क्रीनशॉट आणि संदर्भ क्रमांक सुरक्षित ठेवा",
    recoveryContactBankTitle: "3. बँकेच्या अधिकृत नंबरवर त्वरित संपर्क साधून व्यवहार थांबवण्याची विनंती करा",
    recoveryReportTitle: "4. राष्ट्रीय सायबर पोर्टल (cybercrime.gov.in / 1930) वर तक्रार नोंदवा",
    recoveryDeviceSecurityTitle: "5. नेट बँकिंगचे पासवर्ड आणि यूपीआय पिन त्वरित बदला",

    timelineTitle: "घटनाक्रम कालमर्यादा",
    timelineSubtitle: "दिलेल्या पुराव्यांवर आणि आपल्या माहितीवर आधारित घटनाक्रम",

    trustBreakpointTitle: "आपण कोठे थांबावे?",
    trustBreakpointBadge: "विश्वास खंड बिंदू (TRUST BREAKPOINT)",
    trustBreakpointStopPrefix: "पैसे पाठवण्यापूर्वी थांबा",
    trustBreakpointStopGeneric: "पैसे पाठवण्यापूर्वी थांबा",
    trustBreakpointWhy: "का थांबायचे?",
    trustBreakpointSupportingSignals: "संबंधित संशयास्पद संकेत",
    trustBreakpointViewEvidence: "संबंधित पुरावे पहा",
    trustBreakpointRecommendedStop: "थांबण्याची शिफारस केलेली जागा",
    trustBreakpointNoExplicitPayment: "पैसे भरण्याची कोणतीही थेट मागणी आढळली नाही",
    trustBreakpointNoExplicitPaymentDesc: "काही संशयास्पद संकेत आढळले आहेत, परंतु पैसे पाठवण्याची कोणतीही विशिष्ट रक्कम किंवा मागणी या मजकुरात दिसली नाही.",
    trustBreakpointInsufficientEvidence: "थांबण्याचा बिंदू ठरवण्यासाठी अपुरे पुरावे",
    trustBreakpointSimpleModeExplanation: "रक्षास्कॅनने असा टप्पा शोधून काढला आहे जिथे आपल्याकडे पैसे मागितले जात आहेत. पैसे पाठवण्यापूर्वी येथेच थांबा आणि खात्री करा.",

    claimSpotlightTitle: "दावा → पुरावा विस्तार (Spotlight)",
    claimSpotlightSource: "स्रोत",
    claimSpotlightObservation: "निरीक्षण",
    claimSpotlightVerification: "पडताळणी स्थिती",
    claimSpotlightWhyItMatters: "हे का महत्त्वाचे आहे?",
    claimSpotlightViewEvidence: "पुरावा तपासा",
    claimSpotlightSelectPrompt: "कोणत्याही दाव्यावर क्लिक करून त्याची पडताळणी आणि पुरावे तपासा.",

    disclaimerText: "रक्षास्कॅन केवळ पडताळणी व सुरक्षिततेचे मार्गदर्शन करते. हा कोणताही कायदेशीर सल्ला किंवा निकाल नाही.",
    recoveryDisclaimerText: "पैसे किंवा माहिती उघड झाली असल्यास, बँकेच्या अधिकृत क्रमांकाशी त्वरित संपर्क साधा.",
    ocrNoticeTitle: "स्थानिक ओसीआर सूचना",
    plainLanguageActiveNotice: "सोपी भाषा मोड सुरू आहे.",

    errorBackendUnavailable: "रक्षास्कॅन सर्व्हरशी संपर्क होऊ शकला नाही. कृपया बॅकएंड चालू असल्याची खात्री करा.",
    errorTimeout: "विश्लेषण विनंतीची वेळ संपली. कृपया पुन्हा प्रयत्न करा.",
    errorPayloadTooLarge: "प्रस्तुत इनपुट किंवा प्रतिमा खूप मोठी आहे. कृपया लहान पेलोड सबमिट करा.",
    errorUnsupportedMedia: "असमर्थित फाइल फॉरमॅट. कृपया PNG, JPEG, किंवा WEBP इमेज अपलोड करा.",
    errorRateLimited: "खूप जास्त विनंत्या. कृपया पुन्हा प्रयत्न करण्यापूर्वी थोडा वेळ प्रतीक्षा करा.",
    errorGenericAnalysis: "रक्षास्कॅन सध्या विश्लेषण पूर्ण करू शकले नाही. कृपया पुन्हा प्रयत्न करा.",
  },
};

