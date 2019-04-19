"""
Postgresql interface
"""
import psycopg2
import psycopg2.extras
import logging
import time

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

    def __getContentTypeId__(self, project, name):
        """
        Get id of content type.
        :param project: Project code.
        :param name: Content type name.
        :returns: Content type id.
        :raise KeyError: No content type of given project named as input.
        """
        query = f'''
            SELECT id
            FROM content_types
            WHERE project='{project}' AND name='{name}'
        '''
        self.cursor.execute(query)
        try:
            id = self.cursor.fetchone()['id']
        except:
            raise KeyError(f'No content type named "{name}" found in project "{project}".')
        return id


    def __getResourceTypeId__(self, project, contentType, name):
        """
        Get id of resource type.
        :param project: Project code.
        :param contentType: Content type name.
        :param name: Resource type name.
        :returns: Content type id.
        :raise KeyError: No resource type of given content type of given project named as input.
        """
        contenttype_id = self.__getContentTypeId__(project, contentType)

        query = f'''
            SELECT id
            FROM resource_types
            WHERE content_type='{contenttype_id}' AND name='{name}'
        '''
        self.cursor.execute(query)
        try:
            id = self.cursor.fetchone()['id']
        except:
            raise KeyError(f'No resource type named "{name}" found in content type "{contentType}" of project "{project}".')
        return id


    def __getContentId__(self, project, contentType, name):
        """
        Get id of content.
        :param project: Project code.
        :param contentType: Content type name.
        :param name: Content name.
        :returns: Content id.
        :raise KeyError: No content of given content type of given project named as input.
        """
        contenttype_id = self.__getContentTypeId__(project, contentType)

        query = f'''
            SELECT id
            FROM contents
            WHERE type='{contenttype_id}' AND name='{name}'
        '''
        self.cursor.execute(query)
        try:
            id = self.cursor.fetchone()['id']
        except:
            raise KeyError(f'No content type named "{name}" found in content type "{contentType}" of project "{project}".')
        return id


    def __getUserId__(self, username):
        """
        Get id of user using its username.

        :param username: Username to look up for.
        :returns: User id.
        :raise KeyError: No user with given username found.
        """
        query = f'''
            SELECT id
            FROM users
            WHERE username='{username}'
        '''
        self.cursor.execute(query)
        try:
            id = self.cursor.fetchone()['id']
        except:
            raise KeyError(f'No user with username "{username}" found.')
        return id


    def insertUser(self, username, nicename, email):
        """
        Insert new user.
        
        :param username: Machine friendly username.
        :param nicename: Display name. Usually first, middle and last name of the real person.
        :param email: Full email address.
        """
        query = f'''
            INSERT INTO users (username, nicename, email) VALUES
            ('{username}', '{nicename}', '{email}')
        '''
        self.cursor.execute(query)
        self.connection.commit()


    def insertProject(self, code, name):
        """
        Insert new project.
        
        :param code: An unique short code to identify project.
        :param name: Display name of the project.
        """
        query = f'''
            INSERT INTO projects (code, name) VALUES
            ('{code}', '{name}')
        '''
        self.cursor.execute(query)
        self.connection.commit()

    
    def insertContentType(self, project, name):
        """
        Insert new content type for project.

        :param project: Project code.
        :param name: Name of the content type to add.
        """
        query = f'''
            INSERT INTO content_types (project, name) VALUES
            ('{project}', '{name}')
        '''
        
        self.cursor.execute(query)
        self.connection.commit()


    def insertContent(self, project, contentType, name):
        """
        Insert new content.

        :param project: Project code.
        :param contentType: Content type name.
        :param name: Name of new content.
        :raise KeyError: No content type of given project named as input.
        """
        type_id = self.__getContentTypeId__(project, contentType)

        query = f'''
            INSERT INTO contents (type, name) VALUES
            ('{type_id}', '{name}')
        '''
        self.cursor.execute(query)
        self.connection.commit()


    def insertResourceType(self, project, contentType, name):
        """
        Insert new resource type.

        :param project: Project code.
        :param contentType: Content type name.
        :param name: Name of new resource type.
        :raise KeyError: No content type of given project named as input.
        """
        type_id = self.__getContentTypeId__(project, contentType)

        query = f'''
            INSERT INTO resource_types (content_type, name) VALUES
            ('{type_id}', '{name}')
        '''
        self.cursor.execute(query)
        self.connection.commit()


    def insertNewVersion(self, project, contentType, content, resourceType, creator):
        """
        Insert new version of resource.

        :param project: Project code.
        :param contentType: Content type name.
        :param content: Content name.
        :param resourceType: Resource type name.
        :param creator: Name of the user who's creating
        """
        user_id = self.__getUserId__(creator)
        resourcetype_id = self.__getResourceTypeId__(project, contentType, resourceType)
        content_id = self.__getContentId__(project, contentType, content)

        last_version = self.getLastVersion(project, contentType, content, resourceType)
        new_version = last_version + 1

        query = f'''
            INSERT INTO resource_versions 
                (resource_type, content, version, created_by) VALUES
                ('{resourcetype_id}', '{content_id}', '{new_version}', '{user_id}')
        '''
        self.cursor.execute(query)
        self.connection.commit()


    def getLastVersion(self, project, contentType, content, resourceType):
        """
        Version number of most recent version.

        :param project: Project code.
        :param contentType: Content type name.
        :param content: Content name.
        :param resourceType: Resource type name.
        :returns: Last version id.
        """
        resourcetype_id = self.__getResourceTypeId__(project, contentType, resourceType)
        content_id = self.__getContentId__(project, contentType, content)
        query = f'''
            SELECT version
            FROM resource_versions
            WHERE resource_type={resourcetype_id} AND content={content_id}
            ORDER BY version DESC
        '''
        self.cursor.execute(query)
        try:
            ver = self.cursor.fetchone()['version']
        except:
            ver = 0
        return ver

    
    def getProjectOverview(self, project):
        """
        Get a project overview in an hierarchical format.

        :param project: Project code.
        :returns: A dictionary like this:
            {
                '<content_type1>': {
                    '<content_type1_content1>': {
                        '<content_type1_resource_type1>':
                            (<number_highest_version_resource_type1>, '<status_highest_version_resource_type1>'), 
                        '<content_type1_resource_type2>':
                            (<number_highest_version_resource_type2>, '<status_highest_version_resource_type2>'), 
                        ...
                        '<content_type1_resource_typeN>':
                            (<number_highest_version_resource_typeN>, '<status_highest_version_resource_typeN>')
                    },
                    '<content_type1_content2>': {...},
                    ...
                    '<content_type1_contentM>': {...}
                },
                '<content_type2>': {...},
                ...
                '<content_typeO>': {...}
            }
        """

        # Prepare data structure

        # Fetch content types
        query = f'''
            SELECT id, name
            FROM content_types
            WHERE project = '{project}'
        '''
        self.cursor.execute(query)
        content_types = self.cursor.fetchall()
        out = {}
        for ct in content_types:
            out[ct['name']] = {}

            query = f'''
                SELECT name
                FROM resource_types
                WHERE content_type='{ct['id']}'
            '''
            self.cursor.execute(query)
            resource_types = self.cursor.fetchall()
            
            query = f'''
                SELECT name
                FROM contents
                WHERE type='{ct['id']}'
            '''
            self.cursor.execute(query)
            contents = self.cursor.fetchall()

            for c in contents:
                out[ct['name']][c['name']] = {rt['name']: (None, None) for rt in resource_types}

        # Fill structure with actual data
        query = f'''
            SELECT DISTINCT ON(ct.name, c.name, rt.name)
                ct.name    AS content_type,
                c.name     AS content,
                rt.name    AS resource_type,
                rv.version AS version,
                rv.status  AS status
            FROM
                resource_versions AS rv,
                resource_types    AS rt,
                contents          AS c,
                content_types     AS ct
            WHERE
                ct.project       = '{project}' AND
                c.type           = ct.id       AND
                rt.content_type  = ct.id       AND
                rv.content       = c.id        AND
                rv.resource_type = rt.id
            ORDER BY
                ct.name,
                c.name,
                rt.name,
                rv.version DESC,
                rv.status;
        '''
        self.cursor.execute(query)
        versions = self.cursor.fetchall()

        for v in versions:
            out[v['content_type']][v['content']][v['resource_type']] = (v['version'], v['status'])

        return out


    def firstSetup(self):
        """
        Gives a fresh start to the DB. 
        Remember to create the DB before calling this function.
        BEWARE: This function drops all data in DB!
        """
        query = '''
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;
            GRANT ALL ON SCHEMA public TO postgres;
            GRANT ALL ON SCHEMA public TO public;
            COMMENT ON SCHEMA public IS 'standard public schema';

            CREATE TABLE projects (
                code          varchar(10) PRIMARY KEY,
                name          varchar(50)
            );

            CREATE TABLE users (
                id            serial PRIMARY KEY,
                username      varchar(50) UNIQUE,
                nicename      varchar(100),
                email         varchar(50)
            );

            CREATE TABLE content_types (
                id            serial PRIMARY KEY,
                project       varchar(10) REFERENCES projects(code),
                name          varchar(50) UNIQUE
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
                status        version_status DEFAULT 'inactive',
                creation_date timestamp DEFAULT 'now',
                upload_date   timestamp,
                last_change   timestamp,
                created_by    integer REFERENCES users(id),
                assigned_to   integer REFERENCES users(id),
                updated_by    integer REFERENCES users(id),
                PRIMARY KEY (id, resource_type, content, version)
            );
        '''
        self.cursor.execute(query)
        self.connection.commit()
