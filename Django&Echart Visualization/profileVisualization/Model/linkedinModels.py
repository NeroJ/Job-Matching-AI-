# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Education(models.Model):
    e_id = models.AutoField(primary_key=True)
    p = models.ForeignKey('Profile', models.DO_NOTHING)
    school_name = models.CharField(db_column='School_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    field_study = models.CharField(db_column='Field_Study', max_length=255, blank=True, null=True)  # Field name made lowercase.
    degree_name = models.CharField(db_column='Degree_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    start_date = models.DateField(db_column='Start_Date', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(db_column='End_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Education'


class Honor(models.Model):
    h_id = models.AutoField(primary_key=True)
    p = models.ForeignKey('Profile', models.DO_NOTHING)
    honor_title = models.CharField(db_column='Honor_Title', max_length=255, blank=True, null=True)  # Field name made lowercase.
    issuer = models.CharField(db_column='Issuer', max_length=255, blank=True, null=True)  # Field name made lowercase.
    issue_date = models.DateField(db_column='Issue_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Honor'


class Organization(models.Model):
    o_id = models.AutoField(primary_key=True)
    p = models.ForeignKey('Profile', models.DO_NOTHING)
    org_name = models.CharField(db_column='Org_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    start_date = models.DateField(db_column='Start_Date', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(db_column='End_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Organization'


class Patent(models.Model):
    pat_id = models.AutoField(primary_key=True)
    p = models.ForeignKey('Profile', models.DO_NOTHING)
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)  # Field name made lowercase.
    issuer = models.CharField(db_column='Issuer', max_length=255, blank=True, null=True)  # Field name made lowercase.
    patent_number = models.CharField(db_column='Patent_Number', max_length=255, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=255, blank=True, null=True)  # Field name made lowercase.
    patent_time = models.DateField(db_column='Patent_Time', blank=True, null=True)  # Field name made lowercase.
    patent_detail = models.CharField(db_column='Patent_Detail', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Patent'


class Profile(models.Model):
    p_id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    linkedin = models.CharField(db_column='LinkedIn', unique=True, max_length=255)  # Field name made lowercase.
    occupation = models.CharField(db_column='Occupation', max_length=255, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.
    summary = models.TextField(db_column='Summary', blank=True, null=True)  # Field name made lowercase.
    connection_num = models.IntegerField(db_column='Connection_Num', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Profile'


class Project(models.Model):
    pro_id = models.AutoField(primary_key=True)
    p = models.ForeignKey(Profile, models.DO_NOTHING)
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    start_date = models.DateField(db_column='Start_Date', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(db_column='End_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Project'


class Publication(models.Model):
    pub_id = models.AutoField(primary_key=True)
    p = models.ForeignKey(Profile, models.DO_NOTHING)
    pub_name = models.CharField(db_column='Pub_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    publisher = models.CharField(db_column='Publisher', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Publication'


class Skills(models.Model):
    s_id = models.AutoField(primary_key=True)
    p = models.ForeignKey(Profile, models.DO_NOTHING)
    skill_name = models.CharField(db_column='Skill_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    endorsement = models.IntegerField(db_column='Endorsement', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Skills'


class Volunteer(models.Model):
    v_id = models.AutoField(primary_key=True)
    p = models.ForeignKey(Profile, models.DO_NOTHING)
    company_name = models.CharField(db_column='Company_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=255, blank=True, null=True)  # Field name made lowercase.
    start_date = models.DateField(db_column='Start_Date', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(db_column='End_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Volunteer'


class Workingexperience(models.Model):
    we_id = models.AutoField(primary_key=True)
    p = models.ForeignKey(Profile, models.DO_NOTHING)
    company_name = models.CharField(db_column='Company_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    start_date = models.DateField(db_column='Start_Date', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(db_column='End_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WorkingExperience'

