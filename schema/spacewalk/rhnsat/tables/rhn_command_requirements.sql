--
-- Copyright (c) 2008 Red Hat, Inc.
--
-- This software is licensed to you under the GNU General Public License,
-- version 2 (GPLv2). There is NO WARRANTY for this software, express or
-- implied, including the implied warranties of MERCHANTABILITY or FITNESS
-- FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
-- along with this software; if not, see
-- http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
-- 
-- Red Hat trademarks are not licensed under GPLv2. No permission is
-- granted to use or replicate Red Hat trademarks that are incorporated
-- in this software or its documentation. 
--
--
--
--
--

--reference table
--command_requirements current prod row count = 12
create table 
rhn_command_requirements
(
    name        varchar2 (40)
        constraint rhn_creqs_name_nn not null
        constraint rhn_creqs_name_pk primary key
            using index tablespace [[64k_tbs]]
            ,
    description varchar2 (4000)
        constraint rhn_creqs_description_nn not null
)
    enable row movement
  ;

comment on table rhn_command_requirements 
    is 'creqs storage for system requirements for commands';

--
--Revision 1.2  2004/04/16 21:49:57  kja
--Adjusted small table sizes.  Documented small tables that are primarily static
--as "reference tables."  Fixed up a few syntactical errs.
--
--Revision 1.1  2004/04/12 22:41:48  kja
--More monitoring schema.  Tweaked some sizes/syntax on previously added scripts.
--
