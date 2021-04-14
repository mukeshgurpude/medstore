# TO convert size into readable text
def naturalsize(count):
    f_count = float(count)
    k = 1024
    m = k * k
    g = m * k
    if f_count < k:
        return str(count) + 'B'
    if k <= f_count < m:
        return str(int(f_count / (k / 10.0)) / 10.0) + 'KB'
    if m <= f_count < g:
        return str(int(f_count / (m / 10.0)) / 10.0) + 'MB'
    return str(int(f_count / (g / 10.0)) / 10.0) + 'GB'
