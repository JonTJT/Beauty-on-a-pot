# Beauty on a pot 🍯
Beauty on a pot is a high interaction honeypot that will provide an interface for users to select what type of honeypot they would like to create. For example, users can choose if they want to generate a fake admin page, or a fake contact us page that will act as a honeypot. The user is also able to configure what type of vulnerabilities are present on the honeypot page. After selecting all the necessary parameters, Beauty on a pot will then generate the selected webpage, utilizing the existing web application’s CSS and deploy it to the current web application. After deployment, Beauty on a pot will then log any malicious traffic generated from the honeypot to be examined.

Beauty on a pot aims to improve on existing solutions by easing the process of creating a honeypot. This is achieved by automatically generating honeypot pages on existing web applications, which existing solutions do not provide. 

To test our solution, our team will be creating some web applications using different web servers such as Apache and Nginx before using the tool on them to ensure that the tool will be able to automatically create honeypot pages that are automatically configured and deployed on these web servers, and subsequently ensuring that the malicious activity on our honeypot pages are logged correctly and accurately in our log files. 

# How to use:
Please refer to the [User_Guide](/guides/USERGUIDE.md)
