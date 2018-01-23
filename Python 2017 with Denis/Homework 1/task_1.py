def fibonacci(n):
    if isinstance(n, int) and n >=0:
        if n == 0 or n == 1:
            Fn = 1
        else:
            a = [0]*n
            a[0] = 1
            a[1] = 1
            for i in range(2, n):
                a[i] = a[i-1] + a[i-2]
            Fn = a[-1]
    else:
        Fn = 'Введите целое n >=0 '
    return Fn
