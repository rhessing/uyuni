# coding: utf-8
"""
Test suite for group module of spacecmd
"""

import datetime
import os
from unittest.mock import MagicMock, patch
from helpers import shell, assert_expect, assert_list_args_expect, assert_args_expect
import spacecmd.group


class TestSCGroup:
    """
    Test suite for "group" module.
    """

    def test_group_addsystems_noargs(self, shell):
        """
        Test do_group_addsystems without arguments.

        :param shell:
        :return:
        """

        shell.help_group_addsystems = MagicMock()
        shell.get_system_id = MagicMock()
        shell.expand_systems = MagicMock()
        shell.client.systemgroup.addOrRemoveSystems = MagicMock()
        shell.ssm.keys = MagicMock()
        mprint = MagicMock()
        logger = MagicMock()
        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr:
            spacecmd.group.do_group_addsystems(shell, "")

        assert not shell.get_system_id.called
        assert not shell.ssm.keys.called
        assert not shell.client.systemgroup.addOrRemoveSystems.called
        assert not shell.expand_systems.called
        assert not mprint.called
        assert not logger.error.called
        assert shell.help_group_addsystems.called

    def test_group_addsystems_ssm_no_systems(self, shell):
        """
        Test do_group_addsystems with SSM argument, without systems.

        :param shell:
        :return:
        """
        shell.help_group_addsystems = MagicMock()
        shell.get_system_id = MagicMock()
        shell.expand_systems = MagicMock()
        shell.client.systemgroup.addOrRemoveSystems = MagicMock()
        shell.ssm.keys = MagicMock(return_value=[])
        mprint = MagicMock()
        logger = MagicMock()
        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr:
            spacecmd.group.do_group_addsystems(shell, "groupname ssm")

        assert not shell.get_system_id.called
        assert not shell.expand_systems.called
        assert not shell.client.systemgroup.addOrRemoveSystems.called
        assert not mprint.called
        assert not logger.error.called
        assert not shell.help_group_addsystems.called
        assert shell.ssm.keys.called

    def test_group_addsystems_expand_no_systems(self, shell):
        """
        Test do_group_addsystems with API call to find systems, without success getting one.

        :param shell:
        :return:
        """
        shell.help_group_addsystems = MagicMock()
        shell.get_system_id = MagicMock()
        shell.expand_systems = MagicMock(return_value=[])
        shell.client.systemgroup.addOrRemoveSystems = MagicMock()
        shell.ssm.keys = MagicMock()
        mprint = MagicMock()
        logger = MagicMock()
        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr:
            spacecmd.group.do_group_addsystems(shell, "groupname something*")

        assert not shell.get_system_id.called
        assert not shell.client.systemgroup.addOrRemoveSystems.called
        assert not mprint.called
        assert not logger.error.called
        assert not shell.help_group_addsystems.called
        assert not shell.ssm.keys.called
        assert shell.expand_systems.called

    def test_group_addsystems(self, shell):
        """
        Test do_group_addsystems with API call to find systems.

        :param shell:
        :return:
        """
        shell.help_group_addsystems = MagicMock()
        shell.get_system_id = MagicMock(side_effect=["1000010000", "1000010001"])
        shell.expand_systems = MagicMock(return_value=["one", "two"])
        shell.client.systemgroup.addOrRemoveSystems = MagicMock()
        shell.ssm.keys = MagicMock()
        mprint = MagicMock()
        logger = MagicMock()
        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr:
            spacecmd.group.do_group_addsystems(shell, "groupname something*")

        assert not mprint.called
        assert not logger.error.called
        assert not shell.help_group_addsystems.called
        assert not shell.ssm.keys.called
        assert shell.get_system_id.called
        assert shell.client.systemgroup.addOrRemoveSystems.called
        assert shell.expand_systems.called

        assert_args_expect(shell.client.systemgroup.addOrRemoveSystems.call_args_list,
                           [((shell.session, 'groupname', ['1000010000', '1000010001'], True), {})])

    def test_group_removesystems_noargs(self, shell):
        """
        Test do_group_removesystems without arguments.

        :param shell:
        :return:
        """

        shell.help_group_removesystems = MagicMock()
        shell.get_system_id = MagicMock()
        shell.expand_systems = MagicMock()
        shell.client.systemgroup.addOrRemoveSystems = MagicMock()
        shell.ssm.keys = MagicMock()
        shell.user_confirm = MagicMock()
        mprint = MagicMock()
        logger = MagicMock()
        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr:
            spacecmd.group.do_group_removesystems(shell, "")

        assert not shell.get_system_id.called
        assert not shell.ssm.keys.called
        assert not shell.client.systemgroup.addOrRemoveSystems.called
        assert not shell.expand_systems.called
        assert not shell.user_confirm.called
        assert not mprint.called
        assert not logger.error.called
        assert shell.help_group_removesystems.called

    def test_group_removesystems_ssm_nosys(self, shell):
        """
        Test do_group_removesystems with SSM and without found systems.

        :param shell:
        :return:
        """

        shell.help_group_removesystems = MagicMock()
        shell.get_system_id = MagicMock()
        shell.expand_systems = MagicMock()
        shell.client.systemgroup.addOrRemoveSystems = MagicMock()
        shell.ssm.keys = MagicMock(return_value=[])
        shell.user_confirm = MagicMock()
        mprint = MagicMock()
        logger = MagicMock()
        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr:
            spacecmd.group.do_group_removesystems(shell, "somegroup ssm")

        assert not shell.get_system_id.called
        assert not shell.client.systemgroup.addOrRemoveSystems.called
        assert not shell.expand_systems.called
        assert not shell.user_confirm.called
        assert not logger.error.called
        assert not shell.help_group_removesystems.called
        assert mprint.called
        assert shell.ssm.keys.called

        assert_expect(mprint.call_args_list, "No systems found")

    def test_group_removesystems_nossm_nosys(self, shell):
        """
        Test do_group_removesystems with filters and without found systems.

        :param shell:
        :return:
        """

        shell.help_group_removesystems = MagicMock()
        shell.get_system_id = MagicMock(side_effect=["1000010000", "1000010001"])
        shell.expand_systems = MagicMock(return_value=[])
        shell.client.systemgroup.addOrRemoveSystems = MagicMock()
        shell.ssm.keys = MagicMock()
        shell.user_confirm = MagicMock()
        mprint = MagicMock()
        logger = MagicMock()
        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr:
            spacecmd.group.do_group_removesystems(shell, "somegroup somesystem")

        assert not shell.get_system_id.called
        assert not shell.client.systemgroup.addOrRemoveSystems.called
        assert not shell.user_confirm.called
        assert not logger.error.called
        assert not shell.help_group_removesystems.called
        assert not shell.ssm.keys.called
        assert mprint.called
        assert shell.expand_systems.called

        assert_expect(mprint.call_args_list, "No systems found")

    def test_group_removesystems_nossm_sys(self, shell):
        """
        Test do_group_removesystems with filters and found systems.

        :param shell:
        :return:
        """

        shell.help_group_removesystems = MagicMock()
        shell.get_system_id = MagicMock(side_effect=["1000010000", "1000010001"])
        shell.expand_systems = MagicMock(return_value=["one", "two"])
        shell.client.systemgroup.addOrRemoveSystems = MagicMock()
        shell.ssm.keys = MagicMock()
        shell.user_confirm = MagicMock(return_value=True)
        mprint = MagicMock()
        logger = MagicMock()
        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr:
            spacecmd.group.do_group_removesystems(shell, "somegroup somesystem")

        assert not logger.error.called
        assert not shell.help_group_removesystems.called
        assert not shell.ssm.keys.called
        assert shell.get_system_id.called
        assert shell.user_confirm.called
        assert mprint.called
        assert shell.expand_systems.called
        assert shell.client.systemgroup.addOrRemoveSystems.called

        assert_args_expect(shell.client.systemgroup.addOrRemoveSystems.call_args_list,
                           [((shell.session, 'somegroup', ['1000010000', '1000010001'], False), {})])
        assert_list_args_expect(mprint.call_args_list,
                                ["Systems", "-------", "one\ntwo"])

    def test_group_create_noarg(self, shell):
        """
        Test do_group_create without no arguments (fall-back to the interactive mode).

        :param shell:
        :return:
        """
        msg = "Great group for nothing"
        shell.client.systemgroup.create = MagicMock()
        prompter = MagicMock(side_effect=["Jeff", msg])

        with patch("spacecmd.group.prompt_user", prompter):
            spacecmd.group.do_group_create(shell, "")

        assert prompter.called
        assert shell.client.systemgroup.create.called

        assert_args_expect(shell.client.systemgroup.create.call_args_list,
                           [((shell.session, 'Jeff', msg), {})])

    def test_group_create_name_only(self, shell):
        """
        Test do_group_create with name argument (half-fall back to interactive).

        :param shell:
        :return:
        """
        msg = "Great group for nothing"
        shell.client.systemgroup.create = MagicMock()
        prompter = MagicMock(return_value=msg)

        with patch("spacecmd.group.prompt_user", prompter):
            spacecmd.group.do_group_create(shell, "Jeff")

        assert prompter.called
        assert shell.client.systemgroup.create.called

        assert_args_expect(shell.client.systemgroup.create.call_args_list,
                           [((shell.session, 'Jeff', msg), {})])

    def test_group_create_descr_only(self, shell):
        """
        Test do_group_create with all arguments.

        :param shell:
        :return:
        """
        msg = "Great group for nothing"
        shell.client.systemgroup.create = MagicMock()
        prompter = MagicMock(return_value=msg)

        with patch("spacecmd.group.prompt_user", prompter):
            spacecmd.group.do_group_create(shell, "Jeff {}".format(msg))

        assert not prompter.called
        assert shell.client.systemgroup.create.called

        assert_args_expect(shell.client.systemgroup.create.call_args_list,
                           [((shell.session, 'Jeff', msg), {})])

    def test_group_delete_noarg(self, shell):
        """
        Test do_group_delete without no arguments

        :param shell:
        :return:
        """
        shell.client.systemgroup.delete = MagicMock()
        shell.user_confirm = MagicMock(return_value=False)
        shell.help_group_delete = MagicMock()

        spacecmd.group.do_group_delete(shell, "")

        assert not shell.client.systemgroup.delete.called
        assert not shell.user_confirm.called
        assert shell.help_group_delete.called

    def test_group_delete_no_confirm(self, shell):
        """
        Test do_group_delete no confirmation

        :param shell:
        :return:
        """
        shell.client.systemgroup.delete = MagicMock()
        shell.user_confirm = MagicMock(return_value=False)
        shell.help_group_delete = MagicMock()

        spacecmd.group.do_group_delete(shell, "groupone grouptwo groupthree")

        assert not shell.client.systemgroup.delete.called
        assert not shell.help_group_delete.called
        assert shell.user_confirm.called

    def test_group_delete(self, shell):
        """
        Test do_group_delete with confirmation

        :param shell:
        :return:
        """
        shell.client.systemgroup.delete = MagicMock()
        shell.user_confirm = MagicMock(return_value=True)
        shell.help_group_delete = MagicMock()

        spacecmd.group.do_group_delete(shell, "groupone grouptwo groupthree")

        assert not shell.help_group_delete.called
        assert shell.client.systemgroup.delete.called
        assert shell.user_confirm.called

        groups = [[((shell.session, "groupone"), {})],
                  [((shell.session, "grouptwo"), {})],
                  [((shell.session, "groupthree"), {})],]
        for call in shell.client.systemgroup.delete.call_args_list:
            assert_args_expect([call], next(iter(groups)))
            groups.pop(0)
        assert not groups

    @patch("spacecmd.group.os.path.isdir", MagicMock(return_value=True))
    @patch("spacecmd.group.os.makedirs", MagicMock())
    def test_group_backup_noarg(self, shell):
        """
        Test do_group_backup without no arguments

        :param shell:
        :return:
        """
        shell.help_group_backup = MagicMock()
        shell.do_group_list = MagicMock()
        shell.client.systemgroup.getDetails = MagicMock()
        mprint = MagicMock()
        logger = MagicMock()
        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr:
            spacecmd.group.do_group_backup(shell, "")

        assert not shell.do_group_list.called
        assert not shell.client.systemgroup.getDetails.called
        assert not mprint.called
        assert not logger.called
        assert shell.help_group_backup.called

    @patch("spacecmd.group.os.path.isdir", MagicMock(return_value=True))
    @patch("spacecmd.group.os.makedirs", MagicMock())
    def test_group_backup_all_group_list(self, shell):
        """
        Test do_group_backup with all groups lookup

        :param shell:
        :return:
        """
        def exp_user(path):
            """
            Fake expand user

            :param path:
            :return:
            """
            return os.path.join("/opt/spacecmd", path.replace("~", "").strip("/"))

        shell.help_group_backup = MagicMock()
        shell.do_group_list = MagicMock(return_value=["group-a", "group-b"])
        shell.client.systemgroup.getDetails = MagicMock(
            side_effect=[
                {"description": "Group A description"},
                {"description": "Group B description"},
            ]
        )
        mprint = MagicMock()
        logger = MagicMock()
        opener = MagicMock()
        _open = MagicMock(return_value=opener)

        _datetime = MagicMock()
        _datetime.now = MagicMock(return_value=datetime.datetime(2019, 1, 1))

        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr, \
            patch("spacecmd.group.os.path.expanduser", exp_user) as exu, \
            patch("spacecmd.group.open", _open) as opr, \
            patch("spacecmd.group.datetime", _datetime) as dtm:
            spacecmd.group.do_group_backup(shell, "ALL")

        assert not logger.called
        assert not shell.help_group_backup.called
        assert shell.do_group_list.called
        assert shell.client.systemgroup.getDetails.called
        assert mprint.called
        assert opener.write.called
        assert opener.close.called

        assert_list_args_expect(mprint.call_args_list,
                                ['Backup Group: group-a',
                                 'Output File: /opt/spacecmd/spacecmd-backup/group/2019-01-01/group-a',
                                 'Backup Group: group-b',
                                 'Output File: /opt/spacecmd/spacecmd-backup/group/2019-01-01/group-b'
                                 ])

        assert_list_args_expect(opener.write.call_args_list,
                                ["Group A description", "Group B description"])
        assert_args_expect(_open.call_args_list,
                           [(('/opt/spacecmd/spacecmd-backup/group/2019-01-01/group-a', 'w'), {}),
                            (('/opt/spacecmd/spacecmd-backup/group/2019-01-01/group-b', 'w'), {}),])

    @patch("spacecmd.group.os.path.isdir", MagicMock(return_value=False))
    @patch("spacecmd.group.os.makedirs", MagicMock(side_effect=OSError))
    def test_group_backup_all_group_list_makedirs_failure_handling(self, shell):
        """
        Test do_group_backup with all groups lookup, making directories failure handling.

        :param shell:
        :return:
        """
        def exp_user(path):
            """
            Fake expand user

            :param path:
            :return:
            """
            return os.path.join("/opt/spacecmd", path.replace("~", "").strip("/"))

        shell.help_group_backup = MagicMock()
        shell.do_group_list = MagicMock(return_value=["group-a", "group-b"])
        shell.client.systemgroup.getDetails = MagicMock(
            side_effect=[
                {"description": "Group A description"},
                {"description": "Group B description"},
            ]
        )
        mprint = MagicMock()
        logger = MagicMock()
        opener = MagicMock()
        _open = MagicMock(return_value=opener)

        _datetime = MagicMock()
        _datetime.now = MagicMock(return_value=datetime.datetime(2019, 1, 1))

        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr, \
            patch("spacecmd.group.os.path.expanduser", exp_user) as exu, \
            patch("spacecmd.group.open", _open) as opr, \
            patch("spacecmd.group.datetime", _datetime) as dtm:
            spacecmd.group.do_group_backup(shell, "ALL")

        assert not shell.help_group_backup.called
        assert not shell.client.systemgroup.getDetails.called
        assert not mprint.called
        assert not opener.write.called
        assert not opener.close.called
        assert logger.error.called
        assert shell.do_group_list.called

        assert_args_expect(logger.error.call_args_list,
                           [(('Could not create output directory: %s',
                              '/opt/spacecmd/spacecmd-backup/group/2019-01-01'), {})])

    @patch("spacecmd.group.os.path.isdir", MagicMock(return_value=False))
    @patch("spacecmd.group.os.makedirs", MagicMock(side_effect=OSError))
    def test_group_backup_all_group_list_custom_destination(self, shell):
        """
        Test do_group_backup with all groups lookup, custom destination, handling error.

        :param shell:
        :return:
        """
        def exp_user(path):
            """
            Fake expand user

            :param path:
            :return:
            """
            return os.path.join("/opt/spacecmd", path.replace("~", "").strip("/"))

        shell.help_group_backup = MagicMock()
        shell.do_group_list = MagicMock(return_value=["group-a", "group-b"])
        shell.client.systemgroup.getDetails = MagicMock(
            side_effect=[
                {"description": "Group A description"},
                {"description": "Group B description"},
            ]
        )
        mprint = MagicMock()
        logger = MagicMock()
        opener = MagicMock()
        _open = MagicMock(return_value=opener)

        _datetime = MagicMock()
        _datetime.now = MagicMock(return_value=datetime.datetime(2019, 1, 1, 15, 0, 0))

        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr, \
            patch("spacecmd.group.os.path.expanduser", exp_user) as exu, \
            patch("spacecmd.group.open", _open) as opr, \
            patch("spacecmd.group.datetime", _datetime) as dtm:
            spacecmd.group.do_group_backup(shell, "ALL /dev/null/%Y-%m-%T")

        assert not shell.help_group_backup.called
        assert not shell.client.systemgroup.getDetails.called
        assert not mprint.called
        assert not opener.write.called
        assert not opener.close.called
        assert logger.error.called
        assert shell.do_group_list.called

        assert_args_expect(logger.error.call_args_list,
                           [(('Could not create output directory: %s',
                              '/opt/spacecmd/dev/null/2019-01-15:00:00'), {})])

    @patch("spacecmd.group.os.path.abspath", MagicMock(return_value="/opt/backup"))
    @patch("spacecmd.group.os.listdir", MagicMock(return_value=[]))
    @patch("spacecmd.group.os.path.isdir", MagicMock(return_value=False))
    def test_group_restore_noargs(self, shell):
        """
        test do_group_restore with no arguments.

        :param shell:
        :return:
        """
        shell.help_group_restore = MagicMock()
        shell.do_group_list = MagicMock()
        shell.client.systemgroup.getDetails = MagicMock()
        shell.client.systemgroup.update = MagicMock()
        shell.client.systemgroup.create = MagicMock()
        logger = MagicMock()
        mprint = MagicMock()

        with patch("spacecmd.group.print", mprint) as prn, \
            patch("spacecmd.group.logging", logger) as lgr:
            spacecmd.group.do_group_restore(shell, "")

        assert not shell.do_group_list.called
        assert not shell.client.systemgroup.getDetails.called
        assert not shell.client.systemgroup.update.called
        assert not shell.client.systemgroup.create.called
        assert not logger.debug.called
        assert not logger.error.called
        assert not logger.info.called
        assert not mprint.called

        assert shell.help_group_restore.called

