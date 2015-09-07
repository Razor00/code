#!/usr/bin/python
import math as math
import time as time
from decimal import Decimal
"""
    def reverse_bit(v):
        BitReverseTable256 = [0x00, 0x80, 0x40, 0xC0, 0x20, 0xA0, 0x60, 0xE0, 0x10, 0x90, 0x50, 0xD0, 0x30, 0xB0, 0x70, 0xF0,
                      0x08, 0x88, 0x48, 0xC8, 0x28, 0xA8, 0x68, 0xE8, 0x18, 0x98, 0x58, 0xD8, 0x38, 0xB8, 0x78, 0xF8,
                      0x04, 0x84, 0x44, 0xC4, 0x24, 0xA4, 0x64, 0xE4, 0x14, 0x94, 0x54, 0xD4, 0x34, 0xB4, 0x74, 0xF4,
                      0x0C, 0x8C, 0x4C, 0xCC, 0x2C, 0xAC, 0x6C, 0xEC, 0x1C, 0x9C, 0x5C, 0xDC, 0x3C, 0xBC, 0x7C, 0xFC,
                      0x02, 0x82, 0x42, 0xC2, 0x22, 0xA2, 0x62, 0xE2, 0x12, 0x92, 0x52, 0xD2, 0x32, 0xB2, 0x72, 0xF2,
                      0x0A, 0x8A, 0x4A, 0xCA, 0x2A, 0xAA, 0x6A, 0xEA, 0x1A, 0x9A, 0x5A, 0xDA, 0x3A, 0xBA, 0x7A, 0xFA,
                      0x06, 0x86, 0x46, 0xC6, 0x26, 0xA6, 0x66, 0xE6, 0x16, 0x96, 0x56, 0xD6, 0x36, 0xB6, 0x76, 0xF6,
                      0x0E, 0x8E, 0x4E, 0xCE, 0x2E, 0xAE, 0x6E, 0xEE, 0x1E, 0x9E, 0x5E, 0xDE, 0x3E, 0xBE, 0x7E, 0xFE,
                      0x01, 0x81, 0x41, 0xC1, 0x21, 0xA1, 0x61, 0xE1, 0x11, 0x91, 0x51, 0xD1, 0x31, 0xB1, 0x71, 0xF1,
                      0x09, 0x89, 0x49, 0xC9, 0x29, 0xA9, 0x69, 0xE9, 0x19, 0x99, 0x59, 0xD9, 0x39, 0xB9, 0x79, 0xF9,
                      0x05, 0x85, 0x45, 0xC5, 0x25, 0xA5, 0x65, 0xE5, 0x15, 0x95, 0x55, 0xD5, 0x35, 0xB5, 0x75, 0xF5,
                      0x0D, 0x8D, 0x4D, 0xCD, 0x2D, 0xAD, 0x6D, 0xED, 0x1D, 0x9D, 0x5D, 0xDD, 0x3D, 0xBD, 0x7D, 0xFD,
                      0x03, 0x83, 0x43, 0xC3, 0x23, 0xA3, 0x63, 0xE3, 0x13, 0x93, 0x53, 0xD3, 0x33, 0xB3, 0x73, 0xF3,
                      0x0B, 0x8B, 0x4B, 0xCB, 0x2B, 0xAB, 0x6B, 0xEB, 0x1B, 0x9B, 0x5B, 0xDB, 0x3B, 0xBB, 0x7B, 0xFB,
                      0x07, 0x87, 0x47, 0xC7, 0x27, 0xA7, 0x67, 0xE7, 0x17, 0x97, 0x57, 0xD7, 0x37, 0xB7, 0x77, 0xF7,
                      0x0F, 0x8F, 0x4F, 0xCF, 0x2F, 0xAF, 0x6F, 0xEF, 0x1F, 0x9F, 0x5F, 0xDF, 0x3F, 0xBF, 0x7F, 0xFF]

        c = BitReverseTable256[v & 0xff] << 24 |\
        BitReverseTable256[(v >> 8) & 0xff] << 16 |\
        BitReverseTable256[(v >> 16) & 0xff] << 8 |\
        BitReverseTable256[(v >> 24) & 0xff]

        return c
""" 
class FFT:
    @staticmethod
    def reversed(x, num_bits):
        answer = 0
        for i in range(num_bits):                   # for each bit number
            if (x & (1 << i)):                        # if it matches that bit
                answer |= (1 << (num_bits - 1 - i))   # set the "opposite" bit in answer
        return answer

    @staticmethod
    def get_twiddles(n, p):
        if n == 1:
            return [1]

        fac = [0] * (p)
        wbase = math.e**(-2*math.pi*1j/n) 
        w = 1
        for i in range(p):
            fac[i] = (w)
            w *=  wbase
        return fac

    @staticmethod
    def forward_fft(inp):
        N = len(inp)
        if N == 1:
            return inp

        even = FFT.forward_fft(inp[0::2])   #process even terms  
        odd  = FFT.forward_fft(inp[1::2])   #process odd terms
        W = FFT.get_twiddles(N, N/2)
#        out = [0] * N
        for i in range(N/2):
            inp[i] = even[i] + W[i] * odd[i]
            inp[i+N/2] = even[i] - W[i] * odd[i]
        #print out
        return inp

 
    @staticmethod
    def preprocess(A):
        N = 2**int(math.ceil(math.log(len(A), 2)))
        data = A[:]
        for i in range(N - len(A)):
            data.append(0)
        return data

    @staticmethod
    def DFFT(A):
        data = FFT.preprocess(A)
        out = FFT.forward_fft(data)
        return FFT.reverse_bits(out)
 

    @staticmethod
    def swap_real_imag(A):
        for i in range(len(A)):
            real, imag = A[i].real, A[i].imag
            A[i] = imag + real *1j

    @staticmethod
    def IFFT(A):
        data = A[:]
        FFT.swap_real_imag(data)
        res = [v/len(data) for v in FFT.DFFT(data)]
        FFT.swap_real_imag(res)
        return res

    @staticmethod
    def reverse_bits(A):
        n = int(math.ceil(math.log(len(A), 2)))
        for i in range(len(A)):
            r = FFT.reversed(i, n)
            A[i], A[r] = A[r], A[i]
        return A
   
    @staticmethod
    def multiply(A, B):
        A = A[::-1]
        B = B[::-1]
        la = len(A)
        lb = len(B)
        mlen = lb
        if la > lb:
            mlen = la
        mlen = 2*mlen

        for i in range(mlen - la):    
            A.append(0)

        for i in range(mlen - lb):    
            B.append(0)

        FA = FFT.DFFT(A)
        #print FA
        FB = FFT.DFFT(B)
        #print FB
        m = [FA[i]*FB[i] for i in range(len(FA))]
        m = FFT.IFFT(m)
        #print m
        first = len(m) - 2 #last term is useless, lsb in msb of the  list
        prod = 0L #Decimal(0)
        for v in m[:-1][::-1]:
            prod = prod * 10
            if math.fabs(v.real) > 1e-9:
                prod = prod + int(round(v.real))
        return prod

if __name__ == '__main__':
    import numpy as np
    def DFT_slow(x):
        """Compute the discrete Fourier Transform of the 1D array x"""
        x = np.asarray(x, dtype=float)
        N = x.shape[0]
        n = np.arange(N)
        k = n.reshape((N, 1))
        M = np.exp(-2j * np.pi * k * n / N)
        return np.dot(M, x)

    #a1 = map(float, raw_input("Please enter the data: ").strip().split())
    #a2 = map(float, raw_input("Please enter the data: ").strip().split())
    inp1 = raw_input().strip().split()
    a1 = map(float, inp1)
    inp2 = raw_input().strip().split()
    a2 = map(float, inp2)

    inp1 = "".join(inp1)
    inp2 = "".join(inp2)

    st = time.time()
    fout = FFT.multiply(a1, a2)
    end1 = time.time()

    dout = int(inp1)*int(inp2)
    end2 = time.time()
    assert(fout == dout)
    print "fft = ", end1 - st
    print "normal = ", end2 - end1

"""
    arr = map(float, raw_input("Please enter the data: ").strip().split())
    print  "forward fft"

    dst = FFT.DFFT(arr)  
    print ['{:.2f}'.format(n1) for n1 in dst]

    print  "Reverse fft"
    rdst = FFT.IFFT(dst)  
    print ['{:.2f}'.format(n1) for n1 in rdst]

    import numpy as np
    #print ['{:.2f}'. format(n1) for n1 in np.fft.fft(arr)]
    #print ['{:.2f}'. format(n1) for n1 in np.fft.fftshift(np.fft.fft(arr))]
    print ['{:.2f}'. format(n1) for n1 in DFT_slow(arr)]
"""
