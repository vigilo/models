# -*- coding: utf-8 -*-
"""
Celko's "Nested Sets" Tree Structure.
http://www.intelligententerprise.com/001020/celko.jhtml

With additions from Vigilo team to support
nodes moving and removal.
"""

from sqlalchemy import (select, case, func)
from sqlalchemy.sql.expression import and_
from sqlalchemy.orm import MapperExtension, EXT_CONTINUE, aliased
from sqlalchemy.orm.attributes import instance_state
from vigilo.models.session import DBSession

class CannotRemoveParentException(Exception):
    pass

class CyclicalHierarchyException(Exception):
    pass

class CannotMoveBetweenHierarchiesException(Exception):
    pass

class NestedSetExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        if not instance.parent:
            instance._left = 1
            instance._right = 2
            instance._depth = 0
            return

        cls = mapper.mapped_table
        right_most_sibling = connection.scalar(
            select(
                [cls.c.tree_right]
            ).where(cls.c.idgroup == instance.parent.idgroup)
        )

        connection.execute(
            cls.update(
                and_(
                    cls.c.tree_right >= right_most_sibling,
                    cls.c.grouptype == instance.__class__. \
                        __mapper_args__['polymorphic_identity']
                )
            ).values(
                tree_left = case(
                        [(cls.c.tree_left > right_most_sibling, cls.c.tree_left + 2)],
                        else_ = cls.c.tree_left
                      ),
                tree_right = case(
                        [(cls.c.tree_right >= right_most_sibling, cls.c.tree_right + 2)],
                        else_ = cls.c.tree_right
                      )
            )
        )
        instance._left = right_most_sibling
        instance._right = right_most_sibling + 1
        instance._depth = instance.parent._depth + 1

        p = instance.parent
        while p:
            instance_state(p).expire_attributes(['_left', '_right'])
            p = p.parent

        return EXT_CONTINUE

    def before_update(self, mapper, connection, instance):
        cls = mapper.mapped_table
        left = instance.left
        right = instance.right
        width = right - left + 1

        if not instance.parent:
            return self.before_insert(mapper, connection, instance)

        destination = instance.parent._left + 1
        diff = destination - left
        depthDiff = instance._depth - instance.parent._depth - 1

        # Prépare la place pour le déplacement du nœud.
        connection.execute(
            cls.update(
                and_(
                    cls.c.tree_right >= destination,
                    cls.c.grouptype == instance.__class__. \
                        __mapper_args__['polymorphic_identity'],
                )
            ).values(tree_right = cls.c.tree_right + width)
        )
        connection.execute(
            cls.update(
                and_(
                    cls.c.tree_left >= destination,
                    cls.c.grouptype == instance.__class__. \
                        __mapper_args__['polymorphic_identity'],
                )
            ).values(tree_left = cls.c.tree_left + width)
        )

        # Déplacement du nœud.
        connection.execute(
            cls.update(
                and_(
                    cls.c.tree_right.between(left, right),
                    cls.c.grouptype == instance.__class__. \
                        __mapper_args__['polymorphic_identity'],
                )
            ).values(tree_right = cls.c.tree_right + diff)
        )
        connection.execute(
            cls.update(
                and_(
                    cls.c.tree_left.between(left, right),
                    cls.c.grouptype == instance.__class__. \
                        __mapper_args__['polymorphic_identity'],
                )
            ).values(
                tree_left = cls.c.tree_left + diff,
                _depth = cls.c.depth - depthDiff
            )
        )

        # Suppression des "trous" créés après le déplacement.
        connection.execute(
            cls.update(
                and_(
                    cls.c.tree_right >= left,
                    cls.c.grouptype == instance.__class__. \
                        __mapper_args__['polymorphic_identity'],
                )
            ).values(tree_right = cls.c.tree_right - width)
        )
        connection.execute(
            cls.update(
                and_(
                    cls.c.tree_left >= left,
                    cls.c.grouptype == instance.__class__. \
                        __mapper_args__['polymorphic_identity'],
                )
            ).values(tree_left = cls.c.tree_left - width)
        )
        instance._orig_parent = instance.parent
        return EXT_CONTINUE

    def after_delete(self, mapper, connection, instance):
        cls = mapper.mapped_table
        left = instance.left
        right = instance.right
        width = right - left + 1
        has_parent = bool(instance.parent)

        connection.execute(
            cls.delete(
                and_(
                    cls.c.grouptype == instance.__class__. \
                        __mapper_args__['polymorphic_identity'],
                    cls.c.tree_left.between(left, right)
                )
            )
        )
        connection.execute(
            cls.update(
                and_(
                    cls.c.grouptype == instance.__class__. \
                        __mapper_args__['polymorphic_identity'],
                    cls.c.tree_right > right
                )
            ).values(tree_right = cls.c.tree_right - width)
        )
        connection.execute(
            cls.update(
                and_(
                    cls.c.grouptype == instance.__class__. \
                        __mapper_args__['polymorphic_identity'],
                    cls.c.tree_left > right
                )
            ).values(tree_left = cls.c.tree_left - width)
        )
        return EXT_CONTINUE

    def reconstruct_instance(self, mapper, instance):
        if not instance.idgroup:
            return EXT_CONTINUE

        grouptype = instance.__class__.__mapper_args__['polymorphic_identity']
        cls = instance.__class__
        instance._parent = DBSession.query(
                cls
            ).filter(cls._grouptype == grouptype
            ).filter(cls._depth == instance._depth - 1
            ).filter(cls._left <= instance._left
            ).order_by(cls._left.desc()
            ).first()
        instance._orig_parent = instance._parent
        return EXT_CONTINUE

#def dump_tree(cls):
#    ealias = aliased(cls)
#    for indentation, obj in DBSession.query(
#            func.count(cls.idgroup).label('indentation') - 1,
#            ealias
#        ).join(
#            (ealias, ealias._grouptype == cls._grouptype),
#        ).filter(ealias.left.between(cls.left, cls.right)
#        ).group_by(ealias.idgroup
#        ).order_by(ealias.left):
#        print "    " * indentation + str(obj)
