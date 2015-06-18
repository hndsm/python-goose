import os, sys, json, psycopg2

class _Const(object):

    @apply
    # KNOWN_HOST_REMOVE_SELECTORS
    def get_known_host_remove_selectors():
        def fset(self, value):
            raise SyntaxError
        def fget(self):
            query_string = 'SELECT domains.url, goose_domain_settings.*, domains.url FROM goose_domain_settings INNER JOIN domains ON goose_domain_settings.domain_id=domains.id'
            records = self.get_records_list_by_query(query_string)

            data = {}
            for item in records:
                if item[7]:
                    if item[6] != None : data[item[0]] = item[6]
                    if item[4] != None : data[item[0]] = {'reference' : self.get_domain_reference(records, item[4])}
                    if item[3] != None : data['regexs_references'] = {item[3] : {'reference' : self.get_domain_reference(records, item[4])}}

            return data
        return property(**locals())

    @apply
    # KNOWN_HOST_CONTENT_TAGS
    def get_known_host_content_tags():
        def fset(self, value):
            raise SyntaxError
        def fget(self):
            query_string = 'SELECT domains.url, goose_domain_settings.*, domains.url FROM goose_domain_settings INNER JOIN domains ON goose_domain_settings.domain_id=domains.id'
            records = self.get_records_list_by_query(query_string)

            data = {}
            for item in records:
                if item[7]:
                    if item[5] != None : data[item[0]] = item[5]
                    if item[4] != None : data[item[0]] = {'reference' : self.get_domain_reference(records, item[4])}
                    if item[3] != None : data['regexs_references'] = {item[3] : {'reference' : self.get_domain_reference(records, item[4])}}

            return data
        return property(**locals())

    @apply
    # KNOWN_PUBLISH_DATE_META_TAGS
    def get_known_publish_date_meta_tags():
        def fset(self, value):
            raise SyntaxError
        def fget(self):
            data = self.get_common_settings_list_by_name('KNOWN_PUBLISH_DATE_META_TAGS')
            return data
        return property(**locals())

    @apply
    # KNOWN_DESCRIPTION_META_TAGS
    def get_known_description_meta_tags():
        def fset(self, value):
            raise SyntaxError
        def fget(self):
            data = self.get_common_settings_list_by_name('KNOWN_DESCRIPTION_META_TAGS')
            return data
        return property(**locals())

    @apply
    # KNOWN_CONTENT_TAGS
    def get_known_content_tags():
        def fset(self, value):
            raise SyntaxError
        def fget(self):
            data = self.get_common_settings_list_by_name('KNOWN_CONTENT_TAGS')
            return data
        return property(**locals())

    def get_common_settings_list_by_name(self, name):
        query_string = "SELECT * FROM goose_common_settings WHERE name='%s'" %(name)
        records = self.get_records_list_by_query(query_string)

        common_settings_list = []
        for item in records:
            if item[4]:
                common_settings_list.append({'attribute': item[2], 'value': item[3]})

        return common_settings_list

    def get_records_list_by_query(self, query_string):
        cursor = self.get_connection_cursor()
        cursor.execute(query_string)
        records_list = cursor.fetchall()
        return records_list

    def get_connection_cursor(self):
        try:
            connection_string = "host=%s dbname=%s user=%s password=%s" % (os.environ['DB_HOST'], os.environ['DB_NAME'], os.environ['DB_USER'], os.environ['DB_PASSWORD'])
            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor()
            return cursor
        except:
            print "I am unable to connect to the database"

    def get_domain_reference(self, list, reference_id):
        for item in list:
            if item[1] == reference_id : domain = item[0]
        return domain
