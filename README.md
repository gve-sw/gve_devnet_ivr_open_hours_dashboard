# GVE DevNet IVR Open Hours Dashboard

This sample app provides a dashboard to view and edit an IVR configuration file (JSON) with more ease. Furthermore, it comes with access control based on Microsoft Azure Active Directory and a simple logging mechanisms to prevent unauthorized access and track changes.
This demo does not execute IVR configuration changes itself, but focuses on updating a JSON configuration file. 

## Contacts
* Ramona Renner


## Prepare Microsoft Azure

This demo integrates Microsoft Azure AD for user authentication. Therefore, it incorporates some of the official Microsoft Azure Sample Code for [Integrating Microsoft Identity Platform with a Python web application](https://github.com/Azure-Samples/ms-identity-python-webapp).

Execute the following steps to prepare Microsoft Azure for this demo. The official Microsoft documentation with further information is provided in the section **Further Resources** of this repository.

1. If you do not have an Azure account with active subscription and administrator role, create a free account [here](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) 

2. If you don't have a tenant already, create an [Azure AD B2C tenant](https://learn.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant) that is linked to your Azure subscription.


### Configure a Sign-In User Flow

When users try to sign in to your app, the app starts an authentication request to the authorization endpoint via a user flow. The user flow defines and controls the user experience. After users complete the user flow, Azure AD B2C redirects users back to this demo. 

To add a sign-in policy:   
3. Sign in to the [Azure portal](https://portal.azure.com/).   
4. Select the **Directories + Subscriptions** icon in the portal toolbar.   
5. On the **Portal settings | Directories + subscriptions** page, find your Azure AD B2C directory in the **Directory name** list, and then select **Switch** (if it is not already marked as current).   
6. Search for and select **Azure AD B2C**.   
7. Under **Policies**, select **User flows**, and then select **New user flow**.   
8. On the **Create a user flow** page, select the **Sign in** user flow.   
9. Under **Select a version**, select **Recommended**, and then select **Create**. ([Learn more](https://learn.microsoft.com/en-us/azure/active-directory-b2c/user-flow-versions) about user flow versions.).   
10. Enter the user flow information:  
* Enter a **Name** for the user flow. For example, *signinpasswordreset*.   
* Under **Identity providers** > **Local accounts**, select: **Email signin** for this demo [Further Azure options and information](https://learn.microsoft.com/en-us/azure/active-directory-b2c/sign-in-options).   
* Under **Multifactor authentication**, select **Off** for **MFA enforcement** for this demo. [Further Azure options and information](https://learn.microsoft.com/en-us/azure/active-directory-b2c/multi-factor-authentication).   
* Under **Application claims**, choose **Display Name**.    
11. Click **Create** to add the user flow. A prefix of *B2C_1* is automatically prepended to the name.    
12. Copy and save the user flow name for a later step.   


### Create the Self-service Password Reset User Flow
 
To set up a self-service password reset for the sign-in user flow:   
13. On the **Azure AD B2C** page, select **User flows**.   
14. Select the previously created sign-in user flow to customize it.   
15. In the menu under **Settings**, select **Properties**.   
16. Under **Password configuration**, select **Self-service password reset**.   
17. Click **Save**.   
18. In the left menu under **Customize**, select **Page layouts**.   
19. In **Page Layout Version**, select **2.1.3 or later**.   
20. Select **Save**.   

### Register a Web Application

To enable your application to sign in with Azure AD B2C, register your app in the Azure AD B2C directory. Registering your app establishes a trust relationship between the app and Azure AD B2C.
During app registration, you'll specify the Redirect URI. The redirect URI is the endpoint to which users are redirected by Azure AD B2C after they authenticate with Azure AD B2C. The app registration process generates an Application ID, also known as the client ID, that uniquely identifies your app. After your app is registered, Azure AD B2C uses both the application ID and the redirect URI to create authentication requests.

To create the web app registration, follow these steps:   
21. In the Azure portal, search for and select **Azure AD B2C**.    
22. Select **App registrations**, and then select **New registration**.    
23. Provide the information for the app registration:     
* Under **Name**, enter a name for the application (for example, ivrconfigurator).    
* Under **Supported account types**, select **Accounts in any identity provider or organizational directory (for authenticating users with user flows)**.    
* Under **Redirect URI**, select **Web** and then, in the URL box, enter **http://localhost:5000/getAToken**.    
* Under **Permissions**, select the **Grant admin consent to openid and offline access permissions checkbox**.    
24. Click **Register**.    
25. Select **Overview**.    
26. Copy and save the **Application (client) ID** for later use, when you configure the demo.      


### Create a Web App Client Secret

Create a client secret for the registered web application. The web application uses the client secret to prove its identity when it requests tokens.   

27. Under **Manage**, select **Certificates & secrets**.   
28. Select **New client secret**.   
29. Provide the info for the client secret:    
* In the **Description box**, enter a description for the client secret (for example, ivrconfiguratorsecret).   
* Under **Expires**, select a duration for which the secret is valid, and then select **Add**.   
30. Record the secret's value. You'll use this value for configuration in a later step.   


### Create an Azure User

To create a new user for your organization:    
31. In the Azure portal, search for and select **Users**.    
32. Select **New user**.    
33. On the **New User** page, provide the new user's information:   
* Select **Create Azure AD B2C user** in the section **Select template**    
* Under **Identity**: Select the method **Email** for this demo, since we created a user flow supporting email in a previous step. Add the email address of the user in the next field.    
* Add a **Name** for the user (Name is given and surname of user).   
* Under **Block sign in,** select **No**.    
* Choose the preferred password option. In case of the **auto-generated password** option: Copy the auto-generated password provided in the Password box. You'll need to give this password to the user to sign in for the first time.   
* Provide a **First name** for the user.   
* Provide a **Last Name** for the user.   
34. Select Create.   


## Installation/Configuration

35. Make sure you have [Python 3.8.10](https://www.python.org/downloads/) and [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed.

36. (Optional) Create and activate a virtual environment for the project ([Instructions](https://docs.python.org/3/tutorial/venv.html)).   

37. Access the created virtual environment folder.   
    ```
    cd [add name of virtual environment here] 
    ```

38. Clone this GitHub repository into the local folder:  
    ```
    git clone [add GitHub link here]
    ```
    * For GitHub link: 
      In GitHub, click on the **Clone or download** button in the upper part of the page > click the **copy icon**  
      ![/IMAGES/giturl.png](/IMAGES/giturl.png)
    * Or simply download the repository as zip file using 'Download ZIP' button and extract it.   

39. Access the downloaded folder:  
    ```
    cd gve_devnet_ivr_open_hours_dashboard
    ```

40. Install all dependencies:
    ```
    pip3 install -r requirements.txt
    ```

41. Fill in the variables in the .env file. 

    ```
    CONFIG_PATH=[Fill in local path to IVR configuration file or use example file via ivr-storedb.json]

    TENANT_NAME=[Fill in the first part of your Azure AD B2C tenant name, see also step 2.]
    CLIENT_ID=[Fill in the application (client) ID from step 26]
    CLIENT_SECRET=[Fill in the client secret value you created in step 30]
    SIGNIN_USER_FLOW=[Fill in the name of the user flows you created in step 12, e.g. B2C_1_signinpasswordreset]
    ```

    > **Note:** The content of the **ivr-storedb.json** file of this repository shows the required exemplary format of the IVR configuration file.

    > **Note:** Mac OS hides the .env file in the finder by default. View the demo folder for example with your preferred IDE to make the file visible.

## Usage

42. Run the script:   

```python3 app.py```

Navigate to http://localhost:5000/ and login with the **email** and **password** of an user created in section **Create a Azure User**.


# Screenshots

![/IMAGES/screenshot.png](/IMAGES/screenshot1.png)
![/IMAGES/screenshot.png](/IMAGES/screenshot1.2.png)
![/IMAGES/screenshot.png](/IMAGES/screenshot2.png)
![/IMAGES/screenshot.png](/IMAGES/screenshot3.png)


## Further resources

* [Integrating Microsoft Identity Platform with a Python web application](https://github.com/Azure-Samples/ms-identity-python-webapp)
* [Quickstart: Add sign-in with Microsoft to a web app](https://learn.microsoft.com/en-gb/azure/active-directory/develop/web-app-quickstart?pivots=devlang-python)
* [Configure authentication in a sample Python web app by using Azure AD B2C](https://learn.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-python-web-app)


## LICENSE
Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

## CODE_OF_CONDUCT
Our code of conduct is available [here](CODE_OF_CONDUCT.md)

## CONTRIBUTING
See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without       any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools       is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not          responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
