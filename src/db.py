"""
Postgresql interface
"""
import psycopg2
import psycopg2.extras
import logging

class db(object):

    def __init__(self):
        self.connection = psycopg2.connect(
            dbname='echoes_pm', 
            host='127.0.0.1', 
            user='postgres', 
            password='echoesone')
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        logging.basicConfig(
            format='[%(asctime)s] %(levelname)s: %(message)s', 
            datefmt='%m/%d/%Y %I:%M:%S', 
            level=logging.DEBUG)


    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.close()


    def get_content_types_list(self):
        """
        List all content types
        
        :returns: A dictionary with all content types. 
        """
        query = '''
            SELECT name
            FROM content_types
        '''
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res


    def get_content_type(self, content_type):
        """
        Fetch content type.
        
        :param content_type: Content type name to find.
        :returns: A dictionary with the data of the found row, 
        :raises KeyError: Raises when no content type with given name can be found.
        """
        query = '''
            SELECT name
            FROM content_types
            WHERE name='{0}'
        '''.format(content_type)
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        if res == None:
            raise KeyError('No matching content type found.')
        return res


    def get_contents_list(self, content_type):
        """
        List all contents of given type
        
        :param content_type: Content type name of the contents to list.
        :returns: A dictionary with all content types. 
        """
        query = '''
            SELECT ct.name AS type, c.name AS name
            FROM content_types AS ct, contents AS c 
            WHERE ct.name='{0}' AND c.type=ct.id
        '''.format(content_type)
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        if res == []:
            query = '''
                SELECT name
                FROM content_types
                WHERE name='{0}'
            '''.format(content_type)
            self.cursor.execute(query)
            if self.cursor.rowcount == 0:
                raise KeyError('No matching content type found.')
        return res


    def add_content_type(self, content_type):
        """
        Add content.

        :param content_type: Content type name to add.
        :raises ValueError: Raises when a content type with given name already exists.
        """
        # Check if content doesn't exist
        try:
            self.get_content_type(content_type)
        except:
            pass
        else:
            raise ValueError('Content already exists')
        
        query = '''
            INSERT INTO content_types
            (name) VALUES 
            ('{0}')
        '''.format(content_type)
        self.cursor.execute(query)
        self.connection.commit()


    def get_content(self, content_type, content_name):
        """
        Fetch content.

        :param content_name: The name of the content to find.
        :param content_name: The type of the content to find.
        :returns: A dictionary with the found content.
        :raises KeyError: Raises when no content with given name can be found.
        """
        query = '''
            SELECT ct.name AS type, c.name AS name
            FROM content_types AS ct, contents AS c 
            WHERE ct.name='{0}' AND c.name='{1}' AND c.type=ct.id
        '''.format(content_type, content_name)
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        if res == None:
            raise KeyError('No matching content found.')
        return res


    def add_content(self, content_type, content_name):
        """
        Add content.

        :param content_type: The type of the content to add.
        :param content_name: The name of the content to add.
        :raises ValueError: Raises when the inputs will create a duplicate content.
        :raises KeyError: Raises when no content type with given name can be found.
        """
        # Check if content doesn't exist
        try:
            self.get_content(content_type, content_name)
        except:
            pass
        else:
            raise ValueError('Content already exists')
        
        # Get content type id
        query = '''
            SELECT id
            FROM content_types
            WHERE name='{0}'
        '''.format(content_type)
        self.cursor.execute(query)
        try:
            type_id = self.cursor.fetchone()['id']
        except:
            raise KeyError('No content type named "{0}" found.'.format(content_type))

        # Insert row
        query = '''
            INSERT INTO contents
            (type, name) VALUES 
            ({0}, '{1}')
        '''.format(type_id, content_name)
        self.cursor.execute(query)
        self.connection.commit()


    def get_resources_list(self, content_type, content_name):
        """
        List all resources of given content
        
        :param content_type: Content type name of the content of the resources to list.
        :param content_name: Content name of the resources to list.
        :returns: A dictionary with all the resources of given content. 
        """
        query = '''
            SELECT
                ct.name         AS content_type,
                c.name          AS content_name,
                r.name          AS name
            FROM 
                content_types   AS ct,
                contents        AS c, 
                resources       AS r 
            WHERE
                ct.name     = '{0}' AND 
                c.name      = '{1}' AND 
                c.type      = ct.id AND 
                r.content   = c.id
        '''.format(content_type, content_name)
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        if res == []:
            raise KeyError('No matching content found.')
        for i in range(len(res)):
            res[i] = {
                'content': {
                    'name': res[i]['content_name'],
                    'type': res[i]['content_type'],
                },
                'name': res[i]['name']
            }
        return res


    def get_resource(self, content_type, content_name, resource_name):
        """
        Fetch resource.

        :param content_type: The content type of the resource to find.
        :param content_name: The content name of the resource to find.
        :param resource_name: The name of the resource to find.
        :returns: A dictionary with the found resource.
        :raises KeyError: Raises when no resource with given name can be found.
        """
        # Get resource
        query = '''
            SELECT
                ct.name         AS content_type,
                c.name          AS content_name,
                r.name          AS name,
                r.id            AS id
            FROM 
                content_types   AS ct,
                contents        AS c, 
                resources       AS r 
            WHERE
                ct.name     = '{0}' AND 
                c.name      = '{1}' AND 
                r.name      = '{2}' AND 
                c.type      = ct.id AND 
                r.content   = c.id
        '''.format(content_type, content_name, resource_name)
        self.cursor.execute(query)
        resource = self.cursor.fetchone()
        if resource == None:
            raise KeyError('No content has been found.')
        ret = {
            'content': {
                'name': resource['content_name'],
                'type': resource['content_type'],
            },
            'name': resource['name']
        }
        return ret


    def add_resource(self, content_type, content_name, resource_name):
        """
        Add resource.

        :param content_type: The content type of the resource to add.
        :param content_name: The content name of the resource to add.
        :param resource_name: The name of the resource to add.
        :raises ValueError: Raises when the inputs will create a duplicate resource.
        :raises KeyError: Raises when no content type or content with given names can be found.
        """
        # Check if resource doesn't exist
        try:
            self.get_resource(content_type, content_name, resource_name)
        except:
            pass
        else:
            raise ValueError('Resource already exists')
        
        # Get content type and content ids
        query = '''
            SELECT c.id AS id
            FROM content_types AS ct, contents AS c
            WHERE ct.name='{0}' AND c.name='{1}' AND c.type=ct.id
        '''.format(content_type, content_name)
        self.cursor.execute(query)
        try:
            content_id = self.cursor.fetchone()['id']
        except:
            raise KeyError('No content named "{0}" with type named "{1}" has been found.'.format(content_type, content_name))

        # Insert row
        query = '''
            INSERT INTO resources
            (content, name) VALUES 
            ({0}, '{1}')
        '''.format(content_id, resource_name)
        self.cursor.execute(query)
        self.connection.commit()


    def get_versions_list(self, content_type, content_name, resource_name):
        """
        List all versions of given resources.
        
        :param content_type: Content type name of the resource of the versions to list.
        :param content_name: Content name of the resource of the versions to list.
        :param resource_name: Resource name of the versions to list.
        :returns: A dictionary with all the versions of given resource.
        """
        # Get versions
        query = '''
            SELECT
                v.version       AS version
            FROM 
                content_types       AS ct,
                contents            AS c, 
                resources           AS r,
                resource_versions   AS v
            WHERE
                ct.name     = '{0}' AND 
                c.name      = '{1}' AND 
                r.name      = '{2}' AND 
                c.type      = ct.id AND 
                r.content   = c.id  AND
                v.resource  = r.id
        '''.format(content_type, content_name, resource_name)
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        if res == []:
            raise KeyError('No matching resource found.')

        for i in res:
            i['name'] = 'v{0:0>3}'.format(i['version'])
        return res


    def get_version(self, 
        content_type, content_name, resource_name, version, 
        return_id=False, return_deps=False):
        """
        Fetch resource version.

        :param content_type: The content type of the resource version to find.
        :param content_name: The content name of the resource version to find.
        :param resource_name: The resource name of the resource version to find.
        :param version: The version number of the resource version to find.
        :param return_id: Choose if there will be the version id in the return dict.
        :returns: A dictionary with the found version.
        :raises KeyError: Raises when no version with given input can be found.
        """
        query = '''
            SELECT
                ct.name         AS content_type,
                c.name          AS content_name,
                r.name          AS resource_name,
                v.version       AS version,
                v.id            AS id,
                v.dependencies  AS deps
            FROM 
                content_types       AS ct,
                contents            AS c, 
                resources           AS r,
                resource_versions   AS v
            WHERE
                ct.name     = '{0}' AND 
                c.name      = '{1}' AND 
                r.name      = '{2}' AND 
                v.version   = '{3}' AND
                c.type      = ct.id AND 
                r.content   = c.id  AND
                v.resource  = r.id
                
        '''.format(content_type, content_name, resource_name, version)
        self.cursor.execute(query)
        version = self.cursor.fetchone()
        if version == None:
            raise KeyError('No version has been found.')
        ret = {
            'resource': {
                'name': version['resource_name'],
                'content': {
                    'name': version['content_name'],
                    'type': version['content_type']
                }
            },
            'version': version['version']
        }
        if return_id:
            ret['id'] = version['id']
        if return_deps:
            deps_arr = ','.join(map(str, version['deps']))
            query = '''
                SELECT 
                    ct.name     AS content_type,
                    c.name      AS content_name,
                    r.name      AS resource_name,
                    v.version   AS version 
                FROM 
                    resource_versions   AS v, 
                    resources           AS r, 
                    contents            AS c, 
                    content_types       AS ct 
                WHERE 
                    c.type=ct.id    AND 
                    r.content=c.id  AND 
                    v.resource=r.id AND 
                    v.id=ANY('{{{0}}}');
            '''.format(deps_arr)
            self.cursor.execute(query)
            ret['dependencies'] = []
            for dep in self.cursor:
                ret['dependencies'].append({
                    'resource': {
                        'name': dep['resource_name'],
                        'content': {
                            'name': dep['content_name'],
                            'type': dep['content_type']
                        }
                    },
                    'version': dep['version']
                })
        return ret


    def add_version(self, content_type, content_name, resource_name, version, dependencies):
        """
        Add resource version.

        :param content_type: The content type of the resource version to add.
        :param content_name: The content name of the resource version to add.
        :param resource_name: The resource name of the resource version to add.
        :param version: The version number of the resource version to add.
        :param dependencies: The dependencies, given as a list of tuples 
            (content_type, content_name, resource_name, version), of the resource version to add.
        :raises KeyError: Raises when one of the dependencies cannot be found or 
            when content_type, content_name, resource_name are invalid.
        :raises ValueError: Raises when the inputs will create a duplicate resource.
        """
        # Check if version doesn't exist
        try:
            self.get_version(content_type, content_name, resource_name, version)
        except:
            pass
        else:
            raise ValueError('Version already exists')
        
        # Get resource id
        query = '''
            SELECT r.id AS id
            FROM 
                content_types   AS ct, 
                contents        AS c,
                resources       AS r
            WHERE
                ct.name='{0}'   AND
                c.name='{1}'    AND
                r.name='{2}'    AND
                c.type=ct.id    AND
                r.content=c.id
        '''.format(content_type, content_name, resource_name)
        self.cursor.execute(query)
        try:
            resource_id = self.cursor.fetchone()['id']
        except:
            raise KeyError('No resource with given input has been found.')
        
        # Get dependencies ids
        dependency_ids = []
        for d in dependencies:
            try:
                id = self.get_version(*d, return_id=True)['id']
            except KeyError:
                raise KeyError('Given dependency is not valid')
            dependency_ids.append(str(id))

        # Insert row
        query = '''
            INSERT INTO resource_versions
            (resource, version, dependencies) VALUES 
            ({0}, '{1}', '{{{2}}}')
        '''.format(resource_id, version, ','.join(dependency_ids))
        self.cursor.execute(query)
        self.connection.commit()


    def first_setup(self):
        """
        Gives a fresh start to the DB. 
        Remember to create the DB before calling this function.
        BEWARE: This function drops all tables!

        :param connection: A connection to the Postgres DB.
        """
        with self.connection.cursor() as cur:
            query = '''
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;
            GRANT ALL ON SCHEMA public TO postgres;
            GRANT ALL ON SCHEMA public TO public;
            COMMENT ON SCHEMA public IS 'standard public schema';

            CREATE TABLE projects (
                id            serial PRIMARY KEY,
                name          varchar(50)
            );

            CREATE TABLE users (
                id            serial PRIMARY KEY,
                username      varchar(50),
                nicename      varchar(100),
                email         varchar(50)
            );

            CREATE TABLE content_types (
                id            serial PRIMARY KEY,
                project       integer REFERENCES projects(id),
                name          varchar(50)
            );

            CREATE TABLE IF NOT EXISTS contents (
                id            serial PRIMARY KEY,
                type          integer REFERENCES content_types(id),
                name          varchar(50)
            );

            CREATE TABLE IF NOT EXISTS resource_types (
                id            serial PRIMARY KEY,
                content_type  integer REFERENCES content_types(id),
                name          varchar(50)
            );

            CREATE TYPE version_status AS ENUM (
                'inactive', 
                'assigned', 
                'waiting_review', 
                'approved', 
                'discarded'
            );
            CREATE TABLE IF NOT EXISTS resource_versions (
                id            serial,
                resource_type integer REFERENCES resource_types(id),
                content       integer REFERENCES contents(id),
                version       integer,
                dependencies  integer[],
                status        version_status,
                creation_date date,
                upload_date   date,
                last_change   date,
                created_by    integer REFERENCES users(id),
                assigned_to   integer REFERENCES users(id),
                updated_by    integer REFERENCES users(id),
                PRIMARY KEY (id, resource_type, content, version)
            );'''
            cur.execute(query)
            self.connection.commit()
