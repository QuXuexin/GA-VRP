import numpy as np
import random
import math


def genPopulasi(nPop, nKrom):
    '''

    :param nPop: Jumlah populasi
    :param nKrom: Jumlah kromosom
    :return: Menggenerate populasi sesuai dengan panjang kromosom dan jumlah populasi
    '''
    pop = []
    for i in range(nPop):
        pop.append(np.random.permutation(nKrom))
    return pop


def hitungFitness(node, krom):
    '''

    :param node: Titik koordinat
    :param krom: kromosom
    :return: Nilai fitness dan jarak yang ditempuh pada suatu kromosom
    '''
    jarak = 0
    depot = [82, 76]
    jarak += math.sqrt(sum((a - b) ** 2 for a, b in zip(depot, node[krom[0]])))
    for i in range(len(krom)-1):
        jarak += math.sqrt(sum((a - b) ** 2 for a, b in zip(node[krom[i]], node[krom[i+1]])))
    jarak += math.sqrt(sum((a - b) ** 2 for a, b in zip(node[krom[i+1]], depot)))
    fitness = 1 / (jarak + 0.01)
    return fitness, jarak


def randomParent(nPop):
    '''

    :param nPop: Jumlah populasi
    :return: Random index populasi
    '''
    return int(round(random.uniform(0, nPop)))


def crossover(pCross, krom1, krom2):
    '''

    :param pCross: probabilitas crossover
    :param krom1: parent 1
    :param krom2: parent 2
    :return: hasil crossover antara parent 1 dengan parent 2 menggunakan order crossover dan status apakah crossover
            terjadi atau tidak
    '''
    rand = random.random()
    if rand <= pCross:
        titik1 = int(round(random.uniform(0, len(krom1) - 1)))
        titik2 = int(round(random.uniform(0, len(krom1) - 1)))
        if titik2 < titik1:
            titik1, titik2 = titik2, titik1
        tmp1 = []
        tmp2 = []
        for i in range(titik1, titik2+1):
            tmp1.append(krom1[i])
            tmp2.append(krom2[i])
            krom1[i], krom2[i] = krom2[i], krom1[i]
        j = 0
        for i in range(len(krom1)):
            if i < titik1 or i > titik2:
                if krom1[i] in tmp2:
                    while j < len(tmp1) and tmp1[j] in tmp2:
                        j += 1
                    krom1[i] = tmp1[j]
                    j += 1
        j = 0
        for i in range(len(krom2)):
            if i < titik1 or i > titik2:
                if krom2[i] in tmp1:
                    while j < len(tmp2) and tmp2[j] in tmp1:
                        j += 1
                    krom2[i] = tmp2[j]
                    j += 1
        status = True
    else:
        status = False
    return status, krom1, krom2


def mutasi(pMutasi, krom):
    '''

    :param pMutasi: Probabilitas mutasi
    :param krom: kromosom
    :return: Kromosom yang telah dimutasi
    '''
    rand = random.random()
    if rand <= pMutasi:
        titik1 = int(round(random.uniform(0, len(krom) - 1)))
        titik2 = int(round(random.uniform(0, len(krom) - 1)))
        krom[titik1], krom[titik2] = krom[titik2], krom[titik1]
    return krom


if __name__ == '__main__':

    nGen = 100  # Jumlah genereasi
    nPop = 2000  # Jumlah populasi
    node = [[96, 44], [50, 5], [49, 8], [13, 7], [29, 89], [58, 30], [84, 39], [14, 24], [2, 39], [3, 82], [5, 10],
            [98, 52], [84, 25], [61, 59], [1, 65]]  # Daftar koordinat kota

    pCross = 0.8  # Probabilitas crossover
    pMutasi = 0.4  # Probabilitas mutasi

    # Inisialiasi populasi
    pop = genPopulasi(nPop, len(node))

    for i in range(nGen):

        fitness = []
        jarak = []

        anak = []

        for j in range(nPop/2):

            # Seleksi orang tua
            # Random orang tua
            parent1 = randomParent(nPop-1)
            parent2 = randomParent(nPop-1)

            anak1 = np.copy(pop[parent1])
            anak2 = np.copy(pop[parent2])

            # Crossover
            status, anak1, anak2 = crossover(pCross, anak1, anak2)

            # Mutasi
            if status == True:
                anak1 = mutasi(pMutasi, anak1)
                anak2 = mutasi(pMutasi, anak2)

                anak.append(anak1)
                anak.append(anak2)

        gab = pop + anak
        for f in range(len(gab)):
            fitness.append(hitungFitness(node, gab[f]))
        steadyState = sorted(range(len(fitness)), key=lambda k: fitness[k], reverse=True)
        pop = []
        for j in range(nPop):
            pop.append(gab[steadyState[j]])

    print "\nNilai fitness    :", fitness[steadyState[0]][0]
    print "Jarak terdekat   :", fitness[steadyState[0]][1]
    print "Jalur terdekat   :", 0,
    for i in range(len(pop[0])):
        print pop[0][i]+1,
    print 0
    print "koordinat        :", "[82, 76]",
    for i in range(len(pop[0])):
        print node[pop[0][i]],
    print "[82, 76]"