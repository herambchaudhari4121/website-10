# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DictCode(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    parent_code = models.CharField(db_column='Parent_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lev = models.SmallIntegerField(db_column='Lev', blank=True, null=True)  # Field name made lowercase.
    tpye = models.CharField(db_column='Tpye', max_length=50, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sorted = models.SmallIntegerField(db_column='Sorted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dict_code'


class DictRange(models.Model):
    id = models.BigIntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    parent_code = models.CharField(db_column='Parent_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lev = models.SmallIntegerField(db_column='Lev', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dict_range'


class EquipmentInfo(models.Model):
    eid = models.CharField(db_column='EID', primary_key=True, max_length=20)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    e_code = models.CharField(db_column='E_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    e_name = models.CharField(db_column='E_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    s_code = models.CharField(db_column='S_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    s_name = models.CharField(db_column='S_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    longitude = models.DecimalField(db_column='Longitude', max_digits=9, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    latitude = models.DecimalField(db_column='Latitude', max_digits=8, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='Create_Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'equipment_Info'


class EquipmentExtr(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    eid = models.CharField(db_column='EID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    p_code = models.CharField(db_column='P_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    p_name = models.CharField(db_column='P_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    p_value = models.CharField(db_column='P_Value', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'equipment_extr'


class EquipmentStatus(models.Model):
    eid = models.CharField(db_column='EID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    status_code = models.CharField(db_column='Status_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    status_name = models.CharField(db_column='Status_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status_value = models.SmallIntegerField(db_column='Status_Value', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'equipment_status'


class FeatureHis(models.Model):
    eid = models.CharField(db_column='EID', max_length=20)  # Field name made lowercase.
    obs_time = models.BigIntegerField(db_column='Obs_Time', blank=True, null=True)  # Field name made lowercase.
    feature_info = models.TextField(db_column='Feature_Info', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    years = models.SmallIntegerField(db_column='Years', blank=True, null=True)  # Field name made lowercase.
    opt_time = models.BigIntegerField(db_column='Opt_Time', blank=True, null=True)  # Field name made lowercase.
    at_at1 = models.DecimalField(db_column='AT_AT1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    at_maxat1 = models.DecimalField(db_column='AT_MAXAT1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    at_maxat1t = models.CharField(db_column='AT_MAXAT1T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    at_minat1 = models.DecimalField(db_column='AT_MINAT1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    at_minat1t = models.CharField(db_column='AT_MINAT1T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ah_rh1 = models.DecimalField(db_column='AH_RH1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ah_minrh1 = models.DecimalField(db_column='AH_MINRH1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ah_minrh1t = models.CharField(db_column='AH_MINRH1T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ah_dpt1 = models.DecimalField(db_column='AH_DPT1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ah_wvp1 = models.DecimalField(db_column='AH_WVP1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wd_iwd = models.DecimalField(db_column='WD_IWD', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wd_avg2mwd = models.DecimalField(db_column='WD_AVG2MWD', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wd_avg10mwd = models.DecimalField(db_column='WD_AVG10MWD', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wd_max1miwsd = models.DecimalField(db_column='WD_MAX1MIWSD', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wd_ewsd = models.DecimalField(db_column='WD_EWSD', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wd_exwsd = models.DecimalField(db_column='WD_EXWSD', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ws_iws1 = models.DecimalField(db_column='WS_IWS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ws_avg2mws1 = models.DecimalField(db_column='WS_AVG2MWS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ws_avg10mws1 = models.DecimalField(db_column='WS_AVG10MWS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ws_maxws1 = models.DecimalField(db_column='WS_MAXWS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ws_maxws1t = models.CharField(db_column='WS_MAXWS1T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ws_ews1 = models.DecimalField(db_column='WS_EWS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ws_ews1t = models.CharField(db_column='WS_EWS1T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ws_max1mws1 = models.DecimalField(db_column='WS_MAX1MWS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mntrnfl = models.DecimalField(db_column='MNTRNFL', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    hraccmltrnfl = models.DecimalField(db_column='HRACCMLTRNFL', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_rst = models.DecimalField(db_column='RS_RST', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_maxrst = models.DecimalField(db_column='RS_MAXRST', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_maxrstt = models.CharField(db_column='RS_MAXRSTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rs_minrst = models.DecimalField(db_column='RS_MINRST', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_minrstt = models.CharField(db_column='RS_MINRSTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rs_ct10 = models.DecimalField(db_column='RS_CT10', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_maxct10 = models.DecimalField(db_column='RS_MAXCT10', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_maxct10t = models.CharField(db_column='RS_MAXCT10T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rs_minct10 = models.DecimalField(db_column='RS_MINCT10', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_minct10t = models.CharField(db_column='RS_MINCT10T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ot_fpt = models.DecimalField(db_column='OT_FPT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ot_maxfpt = models.DecimalField(db_column='OT_MAXFPT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ot_maxfptt = models.CharField(db_column='OT_MAXFPTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ot_minfpt = models.DecimalField(db_column='OT_MINFPT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ot_minfptt = models.CharField(db_column='OT_MINFPTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_wft = models.DecimalField(db_column='RW_WFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxwft = models.DecimalField(db_column='RW_MAXWFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxwftt = models.CharField(db_column='RW_MAXWFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_minwft = models.DecimalField(db_column='RW_MINWFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_minwftt = models.CharField(db_column='RW_MINWFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_ift = models.DecimalField(db_column='RW_IFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxift = models.DecimalField(db_column='RW_MAXIFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxiftt = models.CharField(db_column='RW_MAXIFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_minift = models.DecimalField(db_column='RW_MINIFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_miniftt = models.CharField(db_column='RW_MINIFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_sft = models.DecimalField(db_column='RW_SFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxsft = models.DecimalField(db_column='RW_MAXSFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxsftt = models.CharField(db_column='RW_MAXSFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_minsft = models.DecimalField(db_column='RW_MINSFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_minsftt = models.CharField(db_column='RW_MINSFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_snft = models.DecimalField(db_column='RW_SNFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxsnft = models.DecimalField(db_column='RW_MAXSNFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxsnftt = models.CharField(db_column='RW_MAXSNFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_minsnft = models.DecimalField(db_column='RW_MINSNFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_minsnftt = models.CharField(db_column='RW_MINSNFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_trs = models.CharField(db_column='RW_TRS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    av_avg1mhv = models.DecimalField(db_column='AV_AVG1MHV', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    av_minavg10mhv = models.DecimalField(db_column='AV_MINAVG10MHV', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    av_minavg10mhvt = models.CharField(db_column='AV_MINAVG10MHVT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    wetslipcoef = models.CharField(db_column='WETSLIPCOEF', max_length=4, blank=True, null=True)  # Field name made lowercase.
    opt_date = models.DateTimeField(db_column='Opt_Date', blank=True, null=True)  # Field name made lowercase.
    obs_date = models.DateTimeField(db_column='Obs_Date', blank=True, null=True)  # Field name made lowercase.
    pm25 = models.SmallIntegerField(db_column='PM25', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'feature_his'


class FeatureNow(models.Model):
    eid = models.CharField(db_column='EID', max_length=20)  # Field name made lowercase.
    feature_info = models.TextField(db_column='Feature_Info', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    at_at1 = models.DecimalField(db_column='AT_AT1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    at_maxat1 = models.DecimalField(db_column='AT_MAXAT1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    at_maxat1t = models.CharField(db_column='AT_MAXAT1T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    at_minat1 = models.DecimalField(db_column='AT_MINAT1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    at_minat1t = models.CharField(db_column='AT_MINAT1T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ah_rh1 = models.DecimalField(db_column='AH_RH1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ah_minrh1 = models.DecimalField(db_column='AH_MINRH1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ah_minrh1t = models.CharField(db_column='AH_MINRH1T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ah_dpt1 = models.DecimalField(db_column='AH_DPT1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ah_wvp1 = models.DecimalField(db_column='AH_WVP1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wd_iwd = models.DecimalField(db_column='WD_IWD', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wd_avg2mwd = models.DecimalField(db_column='WD_AVG2MWD', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wd_avg10mwd = models.DecimalField(db_column='WD_AVG10MWD', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wd_max1miwsd = models.DecimalField(db_column='WD_MAX1MIWSD', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wd_ewsd = models.DecimalField(db_column='WD_EWSD', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wd_exwsd = models.DecimalField(db_column='WD_EXWSD', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ws_iws1 = models.DecimalField(db_column='WS_IWS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ws_avg2mws1 = models.DecimalField(db_column='WS_AVG2MWS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ws_avg10mws1 = models.DecimalField(db_column='WS_AVG10MWS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ws_maxws1 = models.DecimalField(db_column='WS_MAXWS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ws_maxws1t = models.CharField(db_column='WS_MAXWS1T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ws_ews1 = models.DecimalField(db_column='WS_EWS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ws_ews1t = models.CharField(db_column='WS_EWS1T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ws_max1mws1 = models.DecimalField(db_column='WS_MAX1MWS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mntrnfl = models.DecimalField(db_column='MNTRNFL', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    hraccmltrnfl = models.DecimalField(db_column='HRACCMLTRNFL', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_rst = models.DecimalField(db_column='RS_RST', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_maxrst = models.DecimalField(db_column='RS_MAXRST', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_maxrstt = models.CharField(db_column='RS_MAXRSTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rs_minrst = models.DecimalField(db_column='RS_MINRST', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_minrstt = models.CharField(db_column='RS_MINRSTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rs_ct10 = models.DecimalField(db_column='RS_CT10', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_maxct10 = models.DecimalField(db_column='RS_MAXCT10', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_maxct10t = models.CharField(db_column='RS_MAXCT10T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rs_minct10 = models.DecimalField(db_column='RS_MINCT10', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rs_minct10t = models.CharField(db_column='RS_MINCT10T', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ot_fpt = models.DecimalField(db_column='OT_FPT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ot_maxfpt = models.DecimalField(db_column='OT_MAXFPT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ot_maxfptt = models.CharField(db_column='OT_MAXFPTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ot_minfpt = models.DecimalField(db_column='OT_MINFPT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ot_minfptt = models.CharField(db_column='OT_MINFPTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_wft = models.DecimalField(db_column='RW_WFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxwft = models.DecimalField(db_column='RW_MAXWFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxwftt = models.CharField(db_column='RW_MAXWFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_minwft = models.DecimalField(db_column='RW_MINWFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_minwftt = models.CharField(db_column='RW_MINWFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_ift = models.DecimalField(db_column='RW_IFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxift = models.DecimalField(db_column='RW_MAXIFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxiftt = models.CharField(db_column='RW_MAXIFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_minift = models.DecimalField(db_column='RW_MINIFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_miniftt = models.CharField(db_column='RW_MINIFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_sft = models.DecimalField(db_column='RW_SFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxsft = models.DecimalField(db_column='RW_MAXSFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxsftt = models.CharField(db_column='RW_MAXSFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_minsft = models.DecimalField(db_column='RW_MINSFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_minsftt = models.CharField(db_column='RW_MINSFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_snft = models.DecimalField(db_column='RW_SNFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxsnft = models.DecimalField(db_column='RW_MAXSNFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_maxsnftt = models.CharField(db_column='RW_MAXSNFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_minsnft = models.DecimalField(db_column='RW_MINSNFT', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rw_minsnftt = models.CharField(db_column='RW_MINSNFTT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rw_trs = models.CharField(db_column='RW_TRS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    av_avg1mhv = models.DecimalField(db_column='AV_AVG1MHV', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    av_minavg10mhv = models.DecimalField(db_column='AV_MINAVG10MHV', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    av_minavg10mhvt = models.CharField(db_column='AV_MINAVG10MHVT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    wetslipcoef = models.CharField(db_column='WETSLIPCOEF', max_length=4, blank=True, null=True)  # Field name made lowercase.
    obs_time = models.BigIntegerField(db_column='Obs_Time', blank=True, null=True)  # Field name made lowercase.
    opt_time = models.BigIntegerField(db_column='Opt_Time', blank=True, null=True)  # Field name made lowercase.
    obs_date = models.DateTimeField(db_column='Obs_Date', blank=True, null=True)  # Field name made lowercase.
    opt_date = models.DateTimeField(db_column='Opt_Date', blank=True, null=True)  # Field name made lowercase.
    pm25 = models.SmallIntegerField(db_column='PM25', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'feature_now'


class QualityHis(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    eid = models.CharField(db_column='EID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    years = models.SmallIntegerField(db_column='Years', blank=True, null=True)  # Field name made lowercase.
    obs_time = models.BigIntegerField(db_column='Obs_Time', blank=True, null=True)  # Field name made lowercase.
    opt_time = models.BigIntegerField(db_column='Opt_Time', blank=True, null=True)  # Field name made lowercase.
    quality_info = models.TextField(db_column='Quality_Info', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    opt_date = models.DateTimeField(db_column='Opt_Date', blank=True, null=True)  # Field name made lowercase.
    obs_date = models.DateTimeField(db_column='Obs_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quality_his'


class QualityNow(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    eid = models.CharField(db_column='EID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    obs_time = models.BigIntegerField(db_column='Obs_Time', blank=True, null=True)  # Field name made lowercase.
    opt_time = models.BigIntegerField(db_column='Opt_Time', blank=True, null=True)  # Field name made lowercase.
    quality_info = models.TextField(db_column='Quality_Info', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    opt_date = models.DateTimeField(db_column='Opt_Date', blank=True, null=True)  # Field name made lowercase.
    obs_date = models.DateTimeField(db_column='Obs_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quality_now'


class SensorStatusHis(models.Model):
    eid = models.CharField(db_column='EID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    obs_time = models.BigIntegerField(db_column='Obs_Time', blank=True, null=True)  # Field name made lowercase.
    years = models.SmallIntegerField(db_column='Years', blank=True, null=True)  # Field name made lowercase.
    opt_time = models.BigIntegerField(db_column='Opt_Time', blank=True, null=True)  # Field name made lowercase.
    status_info = models.TextField(db_column='Status_Info', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    extpwrsts1 = models.DecimalField(db_column='EXTPWRSTS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    btryvltgsts1 = models.DecimalField(db_column='BTRYVLTGSTS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    addcvltgsts1 = models.DecimalField(db_column='ADDCVLTGSTS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mainclctrvltgsts = models.DecimalField(db_column='MAINCLCTRVLTGSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mainclctrvltgval = models.DecimalField(db_column='MAINCLCTRVLTGVAL', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mainclctrrunsts = models.DecimalField(db_column='MAINCLCTRRUNSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mainclctradsts = models.DecimalField(db_column='MAINCLCTRADSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mainclctrcntsts = models.DecimalField(db_column='MAINCLCTRCNTSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    solarpanelsts = models.DecimalField(db_column='SOLARPANELSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mothertemp = models.DecimalField(db_column='MOTHERTEMP', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mothertempvalue = models.DecimalField(db_column='MOTHERTEMPVALUE', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    airtmprtsensorsts1 = models.DecimalField(db_column='AIRTMPRTSENSORSTS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    airhmdsensorsts1 = models.DecimalField(db_column='AIRHMDSENSORSTS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    dewpnttmprtsts = models.DecimalField(db_column='DEWPNTTMPRTSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wnddrctsensorsts = models.DecimalField(db_column='WNDDRCTSENSORSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wndspdsensorsts1 = models.DecimalField(db_column='WNDSPDSENSORSTS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rnflsensorsts = models.DecimalField(db_column='RNFLSENSORSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rdtmprtsensorsts = models.DecimalField(db_column='RDTMPRTSENSORSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    cntmtsensorsts = models.DecimalField(db_column='CNTMTSENSORSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    doorsts = models.CharField(db_column='DOORSTS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    gpssts = models.CharField(db_column='GPSSTS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cfspacests = models.DecimalField(db_column='CFSPACESTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    excardsts = models.DecimalField(db_column='EXCARDSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    obs_date = models.DateTimeField(db_column='Obs_Date', blank=True, null=True)  # Field name made lowercase.
    opt_date = models.DateTimeField(db_column='Opt_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sensor_status_his'


class SensorStatusNow(models.Model):
    eid = models.CharField(db_column='EID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    obs_time = models.BigIntegerField(db_column='Obs_Time', blank=True, null=True)  # Field name made lowercase.
    opt_time = models.BigIntegerField(db_column='Opt_Time', blank=True, null=True)  # Field name made lowercase.
    status_info = models.TextField(db_column='Status_Info', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    extpwrsts1 = models.DecimalField(db_column='EXTPWRSTS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    btryvltgsts1 = models.DecimalField(db_column='BTRYVLTGSTS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    addcvltgsts1 = models.DecimalField(db_column='ADDCVLTGSTS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mainclctrvltgsts = models.DecimalField(db_column='MAINCLCTRVLTGSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mainclctrvltgval = models.DecimalField(db_column='MAINCLCTRVLTGVAL', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mainclctrrunsts = models.DecimalField(db_column='MAINCLCTRRUNSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mainclctradsts = models.DecimalField(db_column='MAINCLCTRADSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mainclctrcntsts = models.DecimalField(db_column='MAINCLCTRCNTSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    solarpanelsts = models.DecimalField(db_column='SOLARPANELSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mothertemp = models.DecimalField(db_column='MOTHERTEMP', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    mothertempvalue = models.DecimalField(db_column='MOTHERTEMPVALUE', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    airtmprtsensorsts1 = models.DecimalField(db_column='AIRTMPRTSENSORSTS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    airhmdsensorsts1 = models.DecimalField(db_column='AIRHMDSENSORSTS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    dewpnttmprtsts = models.DecimalField(db_column='DEWPNTTMPRTSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wnddrctsensorsts = models.DecimalField(db_column='WNDDRCTSENSORSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    wndspdsensorsts1 = models.DecimalField(db_column='WNDSPDSENSORSTS1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rnflsensorsts = models.DecimalField(db_column='RNFLSENSORSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rdtmprtsensorsts = models.DecimalField(db_column='RDTMPRTSENSORSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    cntmtsensorsts = models.DecimalField(db_column='CNTMTSENSORSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    doorsts = models.CharField(db_column='DOORSTS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    gpssts = models.CharField(db_column='GPSSTS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cfspacests = models.DecimalField(db_column='CFSPACESTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    excardsts = models.DecimalField(db_column='EXCARDSTS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    obs_date = models.DateTimeField(db_column='Obs_Date', blank=True, null=True)  # Field name made lowercase.
    opt_date = models.DateTimeField(db_column='Opt_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sensor_status_now'


class ServiceStruct(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    parent_code = models.CharField(db_column='Parent_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'service_struct'


class ServiceUser(models.Model):
    user_id = models.CharField(db_column='User_Id', max_length=20, blank=True, null=True)  # Field name made lowercase.
    service_code = models.CharField(db_column='Service_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'service_user'


class WsysUser(models.Model):
    user_name = models.CharField(db_column='User_Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=20, blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='Id', primary_key=True, max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wsys_user'
