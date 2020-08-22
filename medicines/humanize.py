# TO convert size into readable text
def naturalsize(count):
    fcount = float(count)
    k = 1024
    m = k * k
    g = m * k
    if fcount < k: return str(count) + 'B'
    if k <= fcount < m:
        return str(int(fcount / (k / 10.0)) / 10.0) + 'KB'
    if m <= fcount < g:
        return str(int(fcount / (m / 10.0)) / 10.0) + 'MB'
    return str(int(fcount / (g / 10.0)) / 10.0) + 'GB'
