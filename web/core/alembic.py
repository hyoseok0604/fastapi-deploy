from typing import Sequence, TypeGuard

from alembic.autogenerate import produce_migrations
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.operations.ops import MigrateOperation, OpContainer
from sqlalchemy import Connection, MetaData

from web.core.logger import logger


def is_latest(connection: Connection, metadata: MetaData) -> bool:
    migration_context = MigrationContext.configure(connection, opts={"fn": _nothing})
    migration_script = produce_migrations(context=migration_context, metadata=metadata)
    upgrade_ops = migration_script.upgrade_ops

    if upgrade_ops is None:
        return False

    return len(upgrade_ops.ops) == 0


def migration(connection: Connection, metadata: MetaData):
    migration_context = MigrationContext.configure(connection, opts={"fn": _nothing})
    migration_script = produce_migrations(context=migration_context, metadata=metadata)
    upgrade_ops = migration_script.upgrade_ops

    if upgrade_ops is None:
        logger.info("Upgrade Operations is None.")
        return

    ops = Operations(migration_context=migration_context)

    count = _run_operations_recursive(ops, upgrade_ops.ops)

    logger.info(f"Run {count} Operations for migration.")


def _is_op_container(op: MigrateOperation) -> TypeGuard[OpContainer]:
    return issubclass(type(op), OpContainer)


def _run_operations_recursive(
    ops: Operations, migrate_operations: Sequence[MigrateOperation]
) -> int:
    count = 0
    for op in migrate_operations:
        if _is_op_container(op):
            count += _run_operations_recursive(ops, op.ops)
        else:
            ops.invoke(op)
            count += 1
    return count


def _nothing(rev, context):
    return []
