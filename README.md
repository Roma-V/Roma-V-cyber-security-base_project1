# Overview
The application is a simple online clinic.

The users are divided into two groups: doctors and patients. Patients can create records with description of their condition. Doctors can create records on behalf of patients as well as assigning diagnose to a record.

# Security pitfalls
Django is inherently safe, therefore some efforts were required to create vulnerabilities. Below is a list of some built in insecure features and ways they can be addressed.

1. **XSS scripting** - "record_detail.html" template contains vulnerability in showing the symptoms field. "|safe" directive allows for unescaped content, thus enabling scripts to be stored in database and executed on client side. Deleting the directive would instruct Django to escape the content and thus protecting a user. A step further is processing of input strings before putting them into storage. In this case additional protection is provided agains running malicious scripts on the server side.

2. **Broken Access Control** - RecordListView restricts patient to see only their own records, while the RecordDetailView only filters out unauthenticated users. Thus any registered patient can manually navigate to any URL of a record, even those of other patients. A logical extension would be a similar definition of context data to RecordListView - filtering out the records by patient if a patient makes a request and allow full access to doctors.

3. **Sensitive Data Exposure** - continued from the previous paragraph. An authenticated user can access private information of other patients. A proper application design is required in order to prevent data leaks: enforce strict permission rules, prevent logging of sensitive data, enforce encryption while the data is transmitted. The latter is also true about session cookies; setting `SESSION_COOKIE_SECURE=True` would prevent session info from exposure in plain text during transfer via ensuring them being sent under an HTTPS connection.

4. **Broken Authentication** - the application session timeouts aren’t set. When a user uses a public computer to access an application and instead of logging out the user simply closes the browser tab and walks away, an attacker can use the same browser an hour later, and the user is still authenticated. By default `SESSION_COOKIE_AGE=1209600` (2 weeks, in seconds), which makes possible the use of session data left hanging by a user. A reasonably short expiration age might solve the problem. In addition setting `SESSION_EXPIRE_AT_BROWSER_CLOSE=True` will clear the cookies when the browser is closed. `SESSION_COOKIE_SECURE=True` also ensures session data being transferred only via HTTPS.\
Moreover, Django does not throttle requests in user authentication, thus leaving this to a developer discretion to protect against brute-force attacks. A Django plugin or Web server module to throttle these requests are the options one can consider for protection.

5. **Security Misconfiguration** - the application runs on default config. Even though Django has built in security features, many of them are not enabled by default. A thorough analysis of the configuration file in terms of security should be done. Some additional variables that do not have secure defaults and need to be set for better protection might include:
- `SECRET_KEY` - make it secret and unique.
- `SECURE_SSL_REDIRECT=True` - redirect requests over HTTP to HTTPS (requires additional attention in case of sitting behind a proxy).
- `SESSION_COOKIE_SECURE=True` - ensure session data being transferred only via HTTPS.
- `SESSION_EXPIRE_AT_BROWSER_CLOSE=True` - clear session cookies when the browser is closed.
- `SECURE_HSTS_SECONDS=3600` - set "Strict-Transport-Security" header on all HTTPS responses that informs a browser to always use HTTPS in all future connections to the site. Higher values can be a good option that protects infrequent users as well.