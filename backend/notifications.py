"""
Notification system for async email/SMS sending
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models import Notification, User, Question, NotificationType


class NotificationService:
    """Handle all notification operations"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@cosmosastrology.com")
    
    def send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send email via SMTP"""
        try:
            if not self.email_user or not self.email_password:
                print(f"Email credentials not configured. Would send to {to_email}: {subject}")
                return True
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.from_email
            message["To"] = to_email
            
            # Attach HTML
            part = MIMEText(html_content, "html")
            message.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(message)
            
            print(f"Email sent to {to_email}")
            return True
        
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def notify_question_received(self, user: User, question: Question, db: Session):
        """Notify user that their question was received"""
        notification = Notification(
            user_id=user.id,
            type=NotificationType.QUESTION_RECEIVED,
            subject="Your Astrology Question Received",
            message=f"Your question '{question.title}' has been received and is in our queue.",
            related_question_id=question.id
        )
        db.add(notification)
        db.commit()
        
        # Send email
        html_content = f"""
        <html>
            <body style="font-family: Georgia, serif; color: #333;">
                <h2>Your Question Received</h2>
                <p>Dear {user.full_name or user.username},</p>
                <p>We have received your astrology question:</p>
                <p><strong>{question.title}</strong></p>
                <p>An experienced astrologer will be assigned shortly and will provide their insights.</p>
                <p>You will be notified as soon as a response is available.</p>
                <hr>
                <p>Best regards,<br>Cosmos Astrology Team</p>
            </body>
        </html>
        """
        
        self.send_email(user.email, notification.subject, html_content)
    
    def notify_question_assigned(self, user: User, question: Question, astrologer: User, db: Session):
        """Notify user when astrologer is assigned"""
        notification = Notification(
            user_id=user.id,
            type=NotificationType.QUESTION_RECEIVED,
            subject="Astrologer Assigned to Your Question",
            message=f"Astrologer {astrologer.full_name or astrologer.username} has been assigned to answer your question.",
            related_question_id=question.id
        )
        db.add(notification)
        db.commit()
        
        html_content = f"""
        <html>
            <body style="font-family: Georgia, serif; color: #333;">
                <h2>Astrologer Assigned</h2>
                <p>Dear {user.full_name or user.username},</p>
                <p>Good news! Your question has been assigned to an experienced astrologer:</p>
                <p><strong>{astrologer.full_name or astrologer.username}</strong></p>
                <p>Specialization: {astrologer.specialization or 'General Astrology'}</p>
                <p>Experience: {astrologer.experience_years or 'N/A'} years</p>
                <p>Rating: {astrologer.average_rating}/5.0</p>
                <p>You will receive an update as soon as they provide their response.</p>
                <hr>
                <p>Best regards,<br>Cosmos Astrology Team</p>
            </body>
        </html>
        """
        
        self.send_email(user.email, notification.subject, html_content)
    
    def notify_answer_provided(self, user: User, question: Question, astrologer: User, db: Session):
        """Notify user when answer is provided"""
        notification = Notification(
            user_id=user.id,
            type=NotificationType.ANSWER_PROVIDED,
            subject="Your Astrology Question Has Been Answered",
            message=f"Astrologer {astrologer.full_name or astrologer.username} has provided insights to your question.",
            related_question_id=question.id
        )
        db.add(notification)
        db.commit()
        
        html_content = f"""
        <html>
            <body style="font-family: Georgia, serif; color: #333;">
                <h2>Your Question Has Been Answered</h2>
                <p>Dear {user.full_name or user.username},</p>
                <p>Your astrology question has been answered!</p>
                <p><strong>Question:</strong> {question.title}</p>
                <p><strong>Answered by:</strong> {astrologer.full_name or astrologer.username}</p>
                <p>Log in to our platform to read the complete astrological insights and engage in follow-up discussions.</p>
                <p><a href="https://astrology.cosmosastrology.com/questions/{question.id}" style="background-color: #8B008B; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Answer</a></p>
                <hr>
                <p>Best regards,<br>Cosmos Astrology Team</p>
            </body>
        </html>
        """
        
        self.send_email(user.email, notification.subject, html_content)
    
    def notify_new_consultation_available(self, user: User, astrologer: User, db: Session):
        """Notify user about paid consultation opportunity"""
        notification = Notification(
            user_id=user.id,
            type=NotificationType.NEW_CONSULTATION,
            subject="Schedule a Live Consultation with Your Astrologer",
            message=f"Schedule a personalized consultation with {astrologer.full_name or astrologer.username}"
        )
        db.add(notification)
        db.commit()
        
        html_content = f"""
        <html>
            <body style="font-family: Georgia, serif; color: #333;">
                <h2>Live Consultation Available</h2>
                <p>Dear {user.full_name or user.username},</p>
                <p>{astrologer.full_name or astrologer.username} is now offering live consultations!</p>
                <p>Get personalized astrological guidance directly from an experienced astrologer.</p>
                <p><strong>Rate:</strong> ${astrologer.hourly_rate}/hour</p>
                <p><strong>Experience:</strong> {astrologer.experience_years or 'N/A'} years</p>
                <p><strong>Rating:</strong> {astrologer.average_rating}/5.0</p>
                <p><a href="https://astrology.cosmosastrology.com/astrologers/{astrologer.id}/book" style="background-color: #8B008B; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Book Consultation</a></p>
                <hr>
                <p>Best regards,<br>Cosmos Astrology Team</p>
            </body>
        </html>
        """
        
        self.send_email(user.email, notification.subject, html_content)
    
    def notify_astrologer_new_question(self, astrologer: User, question: Question, user: User, db: Session):
        """Notify astrologer about new question in queue"""
        notification = Notification(
            user_id=astrologer.id,
            type=NotificationType.QUESTION_RECEIVED,
            subject=f"New Question in Queue: {question.category}",
            message=f"A new {question.category} question from {user.full_name or user.username}",
            related_question_id=question.id
        )
        db.add(notification)
        db.commit()
        
        html_content = f"""
        <html>
            <body style="font-family: Georgia, serif; color: #333;">
                <h2>New Question in Queue</h2>
                <p>Dear {astrologer.full_name or astrologer.username},</p>
                <p>A new question in your specialization area is waiting for your expertise:</p>
                <p><strong>Category:</strong> {question.category}</p>
                <p><strong>Title:</strong> {question.title}</p>
                <p><strong>User:</strong> {user.full_name or user.username}</p>
                <p><a href="https://astrology.cosmosastrology.com/dashboard/questions/{question.id}" style="background-color: #20B2AA; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Question</a></p>
                <hr>
                <p>Best regards,<br>Cosmos Astrology Team</p>
            </body>
        </html>
        """
        
        self.send_email(astrologer.email, notification.subject, html_content)


# Global notification service instance
notification_service = NotificationService()
