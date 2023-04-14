import pendulum

TIMEZONE = pendulum.timezone('Asia/Ho_Chi_Minh')

def local_ds(ts, next_date=False):
    """
    Transform timestamp to local execution date string.
    
        Parameters:
            ts (timestamp): Timestamp want to convert
            next_date (bool): if True => (current date + 1)
        Returns:
            local_execution_date (string): date string, E.g: 2000-12-17
    """
    
    if next_date:
        local_execution_date = TIMEZONE.convert(
            pendulum.parse(ts)
        ).replace(
            hour=0, minute=0, second=0, microsecond=0
        ).add(days=1)
    else:
        local_execution_date = TIMEZONE.convert(
            pendulum.parse(ts)
        ).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    return local_execution_date.strftime('%Y-%m-%d')

def local_ds_nodash(ts, subtract_date=None, next_date=False):
    """
    Transform timestamp to local execution date string with no dash.
    
        Parameters:
            ts (timestamp): Timestamp want to convert
            next_date (bool): if True => (current date + 1)
        Returns:
            local_execution_date (string): date string, E.g: 20001217
    """

    if next_date:
        local_execution_date = TIMEZONE.convert(
            pendulum.parse(ts)
        ).replace(
            hour=0, minute=0, second=0, microsecond=0
        ).add(days=1)
    else:
        if subtract_date:
            local_execution_date = TIMEZONE.convert(
                pendulum.parse(ts)
            ).replace(
                hour=0, minute=0, second=0, microsecond=0
            ).subtract(days=subtract_date)
        else:
            local_execution_date = TIMEZONE.convert(
                pendulum.parse(ts)
            ).replace(
                hour=0, minute=0, second=0, microsecond=0
            )

    return local_execution_date.strftime('%Y%m%d')


def local_ts_nodash(ts, next_date=False):
    """
    Transform timestamp to local timestamp string with no dash.
    
        Parameters:
            ts (timestamp): Timestamp want to convert
            next_date (bool): if True => (current date + 1)
        Returns:
            local_execution_date (string): date string, E.g: 20001217
    """

    if next_date:
        local_execution_date = TIMEZONE.convert(
            pendulum.parse(ts)
        ).add(days=1)
    else:
        local_execution_date = TIMEZONE.convert(
            pendulum.parse(ts)
        )
    return local_execution_date.strftime('%Y%m%dT%H%M%S')

