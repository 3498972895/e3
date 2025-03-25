REFACTOR CODE FROM PAPAER&REPO "THREE DYNAMIC PRICING SCHEMES FOR RESOURCE ALLOCATION OF EDGE COMPUTING FOR IOT ENVIRONMENT"

Data FOR TESTING IS SAME WITH PAPER

static_num_users = 5
static_rs = [1, 2, 8, 10, 15] * 8
static_mus = [1, 1.5, 2, 3, 5]
static_cs = [20000, 20000, 31680, 31680, 2640]  # needed cycles per one bit
static_fmax = 8 * 10**3  # GHz

RESULT 

-- BID-PRIM

    buyer's cost: [15.297699387333061, 17.459142212632926, 34.362423692549, 31.885356979901673, 9.900252694799486]
    buyer's resource allocation: [1123.69862978237, 1282.4682774036012, 2524.1055820925185, 2342.151655699623, 727.2270232252791]
    buyer's utility: [-33.096065844248166, -57.37856861968346, -169.13269156819024, -230.91631304617476, -103.95468549395002]
    seller's unit_price: 0.013613702982137976
    seller's utility: 108.90487496492204


-- UNI-PRIM


    buyer's cost: [18.997380353762296, 21.93628532228474, 47.81908945699128, 43.65265662491932, 11.95477236424782]
    buyer's resource allocation: [1052.77673171602, 1215.6418589056373, 2649.9877232913977, 2419.0967552640946, 662.4969308228494]
    buyer's utility: [-37.99476070752459, -65.80885596685422, -191.27635782796511, -261.9159397495159, -119.54772364247819]
    seller's unit_price: 0.018045023015275684
    seller's utility: 144.36018412220545

-- FAID-PRIM


    buyer's cost: [14.724480881902503, 31.80851417142467, 69.33964261998887, 33.83428114553618, 9.26589950019095]
    buyer's resource allocation: [1358.2821805678398, 838.3499626217309, 1827.5260040562978, 3121.094831179294, 854.7470215748388]
    buyer's utility: [-29.448961763805006, -95.42554251427401, -277.35857047995546, -203.0056868732171, -92.65899500190949]
    seller's unit_price: 0.010840516862075615
    seller's utility: 158.97281831904317
    fairness factor: 3.5
    ['price: 0.03794180901726465 group: [1, 2]', 'price: 0.010840516862075615 group: [0, 3, 4]']
