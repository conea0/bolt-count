import cv2
import optuna

def calc(path, params):
    # 画像の読み込み
    image = cv2.imread(path)  # './output/20/20_3_out.JPG'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2値化
    ret, dst = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)

    # 黒白反転する
    dst = cv2.bitwise_not(dst)


    # 円の検出
    circles = cv2.HoughCircles(
        dst, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=params['minDist'],
        param1=params['param1'],
        param2=params['param2'],
        minRadius=params['minRadius'],
        maxRadius=params['maxRadius']
    )

    if circles is not None:
        cnt = len(circles[0])
    else:
        cnt = 0

    return cnt

# ハイパーパラメータの最適化
def objective(trial):
   params = {
        'minDist': trial.suggest_uniform('minDist', 0.1, 5),
        'param1': trial.suggest_int('param1', 0.01, 200),
        'param2': trial.suggest_int('param2', 1, 50),
        'minRadius': 0, # trial.suggest_int('minRadius', 0, 300),
        'maxRadius': 0, # trial.suggest_int('maxRadius', 0, 500)
    }
   
   data = [
      ('./output/15/15_1_out.JPG', 9),
      ('./output/15/15_2_out.JPG', 1),
      ('./output/15/15_3_out.JPG', 3),
      ('./output/15/15_4_out.JPG', 3),
      ('./output/20/20_2_out.JPG', 10),
      ('./output/15/15_2_out.JPG', 1),
      ('./output/25/25_4_out.JPG', 4),
      ('./output/25/25_1_out.JPG', 2),
   ]

   score = 0

   for d in data:
      cnt = calc(d[0], params)
      score += abs(cnt - d[1])
   
   return score

def main():
    study = optuna.create_study()
    study.optimize(objective, n_trials=1000)

    print("-------------------------")
    print('params:', study.best_params)
    print(study.best_value)

if __name__ == '__main__':
    main()