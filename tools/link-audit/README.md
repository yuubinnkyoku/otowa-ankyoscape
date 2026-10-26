# 引用URLの保全監査（link audit）

このリポジトリが引用しているWeb資料について、Wayback Machine への保存状態を点検し、未保存分を保存するための作業ファイル一式。2026年10月25日に実施。

## 結果サマリー（2026-10-25時点）

- 引用URL 1,217件（重複・フラグメント・web.archive.org 自身を除くユニーク 1,202件）を CDX で全数検査
  - 保存済み 536件／未保存 666件／エラー 0件
- 未保存 666件すべてに Save Page Now 2（SPN2）で保存を依頼し、全件受理（job_id 666件）
- 同日夜の再検査で 461件は当日分の保存完了を確認、2件は以前から保存済み（監査時の検出漏れ）、203件は未確定
- 203件の再検査を2026-10-26に実施予定

## ファイル一覧

| ファイル | 内容 |
| --- | --- |
| `all_urls.txt` | 引用URLの全リスト（1,217行） |
| `cdx_progress.jsonl` | CDX検査の進捗ログ（追記式） |
| `archived_urls.txt` | 保存済みURL（タブ区切りで最古の保存時刻付き） |
| `unarchived_urls.txt` | 未保存URL |
| `cdx_errors.txt` | CDX検査で最終的にエラーだったURL（今回は0件で空） |
| `spn2_progress.jsonl` | SPN2投入の記録（URL・job_id・status、全666件） |
| `spn2_results.csv` | SPN2結果の一覧（.ps1版と同じ形式：URL, JobId, Status） |
| `spn2_verify.jsonl` | 投入後の保存確認（verify=captured / not_yet、保存時刻、HTTP状態） |
| `.cdx_check.py` | CDX全数検査スクリプト |
| `.cdx_resume.py` | CDX検査の再開・エラー再試行用スクリプト |
| `.spn2_archive.ps1` | SPN2保存スクリプト（PowerShell版。要 IA_ACCESS_KEY / IA_SECRET_KEY） |
| `.spn2_archive.py` | SPN2保存スクリプト（Python版。キーは標準入力から読み、ファイルに残さない） |

## 注意

- スクリプトはこのフォルダを作業ディレクトリとして実行する前提（相対パスでファイルを参照）。
- `spn2_progress.jsonl` の status=pending は「IAがジョブを受理した」意味であり、保存完了の確認は `spn2_verify.jsonl` 側で行う。

## URLクリーニング（2026-10-26）

再検査で未保存だった203件を精査したところ、144件は抽出時の混入だった
（URL末尾に U+E201 と日本語の続きが付着、末尾バッククォート、括弧の欠落など）。
混入した記法のままでは CDX にヒットしないため「未保存」に見えていた。

- 144件をクリーニングすると実URLは78件に集約される（同一の GitHub README が60件分あった）
- 78件のうち15件は正形URLで保存確認済みだったもの、63件を CDX で再検査し31件の保存を確認
  （1998〜2004年の旧保存を含む。消失サイト系は当初から保存されていた）
- 対応表は url_corrections.jsonl（invalid → cleaned → cleaned_verify）

クリーニング後の実態（SPN2投入対象だった666件について）:
- 実URL総数は 585件（混入144件を実URL78件に置換したため）
- 保存確認できたのは 494件、本当に未保存なのは 91件
  （主なホスト: github.com 32、lotus62ankyo.blog.jp 14、commons.wikimedia.org 6、note.com 6）
- 再投入の要否は、この91件の範囲で判断する

## SPN2再投入（2026-10-26）

本当に未保存だった91件（resubmit_urls.txt）を SPN2 へ再投入した。

- 84件が pending で受理（spn2_resubmit_progress.jsonl 32件＋spn2_resubmit59_progress.jsonl 52件）
- 7件は IA 側が一貫して error を返した（再試行でも同じ）:
  adeac.jp の PDF 2件、commons.wikimedia.org の Special:Redirect ファイルURL 5件
  （spn2_retry7_progress.jsonl）
- 投入後約1時間の CDX 確認で 37件に 2026-10-26 の保存を確認（うち github.com 29件）。
  残り54件は反映待ち（上の error 7件を含む）。結果は spn2_verify.jsonl に追記済み
- 実URL585件のうち保存確認は 531件になった
