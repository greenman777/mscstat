Ext.define('MSCSTAT.model.Users', {
    extend: 'Ext.data.Model',
    fields: [
    	'id',
        'is_superuser',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'phone',
        'phone_other',
        'phone_short',
        'organization_name',
        'organization_phone',
        'organization_fax',
        'business_address',
        'position',
        'rating',
        'birthday'
   ]
});
