import win32com.client
import os
import time

def move_emails_and_save_attachments(search_string, target_folder_name, save_path, number=100, sender=None):
    # Initialize Outlook application
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    
    # Get the default inbox folder
    inbox = namespace.GetDefaultFolder(6)  # 6 refers to the inbox folder
    
    # Get the folder where emails will be moved (under the inbox)
    target_folder = None
    
    # Check if the folder already exists
    for folder in inbox.Folders:
        if folder.Name == target_folder_name:
            target_folder = folder
            break

    # If the target folder doesn't exist, create it
    if not target_folder:
        target_folder = inbox.Folders.Add(target_folder_name)
    
    # Get all items (emails) in the inbox
    messages = inbox.Items
    
    # Sort the messages by ReceivedTime in descending order (newest emails first)
    messages.Sort("[ReceivedTime]", True)
    
    # Track the number of emails processed
    processed_count = 0
    
    # Loop through all messages in the inbox
    for message in messages:
        try:
            # Check if the item is an email (MailItem has Class 43)
            if message.Class == 43:
                subject = message.Subject
                sender_email = message.SenderEmailAddress
                
                # Check if the search string is found in the subject (case-insensitive search)
                if search_string.lower() in subject.lower():
                    
                    # If sender filter is provided, check if sender matches the filter
                    if sender is None or sender.lower() in sender_email.lower():
                        print(f"Processing email with subject: {subject} from sender: {sender_email}")
                        
                        # Check for attachments
                        if message.Attachments.Count > 0:
                            # Loop through each attachment
                            for attachment in message.Attachments:
                                # Define the path to save the attachment
                                attachment_path = os.path.join(save_path, attachment.FileName)
                                
                                # Save the attachment
                                attachment.SaveAsFile(attachment_path)
                                print(f"Saved attachment: {attachment.FileName} to {attachment_path}")
                        
                        # Move the email to the target folder
                        message.Move(target_folder)
                        print(f"Email moved to folder: {target_folder_name}")
                        
                        # Increment the processed email count
                        processed_count += 1
                        
                        # Stop if the specified number of emails has been processed
                        if processed_count >= number:
                            print(f"Processed {processed_count} emails. Stopping.")
                            break
        except Exception as e:
            print(f"Error processing email: {str(e)}")

if __name__ == "__main__":
    # The string to search for in email subjects
    search_string = "Important"
    
    # The folder to move emails to (this folder will be created under Inbox if not already present)
    target_folder_name = "ImportantEmails"
    
    # The directory to save attachments to
    save_path = r"C:\path\to\save\attachments"
    
    # Number of emails to process
    number_to_check = 100
    
    # Sender email filter (part of the sender's email, e.g., '@outlook')
    sender_filter = "@outlook"  # Set this to None to process emails from any sender
    
    # Ensure the save path exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Move emails based on the subject, save attachments, and apply number and sender filters
    move_emails_and_save_attachments(search_string, target_folder_name, save_path, number=number_to_check, sender=sender_filter)
    
    move_emails_and_save_attachments(
    search_string="Project", 
    target_folder_name="ProjectEmails", 
    save_path=r"C:\Users\Documents\EmailAttachments", 
    number=50, 
    sender="@outlook")