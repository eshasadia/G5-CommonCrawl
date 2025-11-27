## dictionary of boiler plat patterns 

# Define boilerplate regex patterns
boilerplate_patterns <- c(
  "skip to main content", "menu", "breadcrumbs", "search", "keyword search",
  "choose text size", "choose a background", "change your pointer",
  "log in", "sign up", "sign in/register", "my accounts",
  "privacy policy", "cookies", "terms and conditions", "legal and disclaimer",
  "accessibility statement", "©", "crown copyright",
  "rate this page", "was this page useful", "thank you for your feedback",
  "report a problem", "loading", "skip back to top", "browser does not support script",
  "facebook", "twitter", "youtube", "linkedin", "instagram",
  "\\b\\d+\\s+page\\s+\\d+\\s+of\\s+\\d+" # pagination pattern
)

