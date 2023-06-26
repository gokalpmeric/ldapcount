import subprocess
import datetime
import re
from collections import defaultdict
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# The location of your log files
log_file_path = "/path/to/your/log/files"

# The current date
date = datetime.date.today().strftime("%Y-%m-%d")

# The grep command to search the log files for LDAP connections
# You will need to adjust the search pattern based on how LDAP connections are logged in your setup
grep_command = f"grep 'LDAP' {log_file_path} | grep '{date}'"

# Run the grep command
grep_output = subprocess.check_output(grep_command, shell=True)

# Split the output into lines
lines = grep_output.decode('utf-8').split('\n')

# Create a dictionary to count the number of connections for each user
user_connections = defaultdict(int)

# Loop through the lines
for line in lines:
    # Search for the username in the line
    # You will need to adjust the search pattern based on how the username is logged in your setup
    match = re.search('username: (\w+)', line)
    if match:
        # If a username was found, increment its count in the dictionary
        user_connections[match.group(1)] += 1

# Create a DataFrame from the dictionary
df = pd.DataFrame(list(user_connections.items()), columns=['User', 'Number of Connections'])

# Write the DataFrame to an Excel file
excel_file = "LDAP_Connections.xlsx"
df.to_excel(excel_file, index=False)

# Email the Excel file
# Set up the SMTP server and the email details
smtp_server = "smtp.yourserver.com"
port = 587  # For starttls
sender_email = "your-email@yourdomain.com"
receiver_email = "abc@gokalp.com"
password = "your-password"

# Create the email message
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = f"LDAP Connections for {date}"

# Attach the Excel file
with open(excel_file, "rb") as f:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(f.read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename= {excel_file}")
msg.attach(part)

# Connect to the server and send the email
server = smtplib.SMTP(smtp_server, port)
server.starttls()  # Secure the connection
server.login(sender_email, password)
server.send_message(msg)
server.quit()

