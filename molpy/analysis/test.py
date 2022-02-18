from multiprocessing import Pool
import numpy as np
from time import sleep, time

def f(X):
    if X[0] == 3:
        raise ValueError
        # return 'err'
    sleep(3)
    return X**2



if __name__ == '__main__':
    results = []
    start = time()
    with Pool(5) as p:

        # results.append(p.apply_async(f, np.arange(15).reshape((5,3)), 1, lambda x: f'ans: {x}', lambda e: print('err')))
        for i in np.arange(15).reshape((5,3)):
            a = p.apply_async(f, (i, ))
            results.append(a)
            sleep(4)
            print(a.ready())
        
        for res in results:
            print(res.ready())
        p.join()
        
    end = time()
    print(end-start)

    ans = []
    for res in results:
 
        print(res.ready())
        try:
            a = res.get()
            ans.append(a)
        except:
            ans.append('err')
    print(ans)
