# 全模块路由与实际PDF覆盖

本表按实际原PDF页序建立，不使用已错位的原目录页码。所有主题技能都自带其原页。

| 模块 | 技能调用名 | 主要原PDF页序 |
|---|---|---|
| 津上S205A/S206A｜手册总导航 | `$tsugami-s20a-manual` | 1–18 |
| 津上S205A/S206A｜安全与联锁 | `$tsugami-s20a-safety` | 17–26、56、157–164 |
| 津上S205A/S206A｜结构规格与备件 | `$tsugami-s20a-specifications` | 27–48、262–268 |
| 津上S205A/S206A｜搬运安装与首次通电 | `$tsugami-s20a-installation` | 17–18、49–55 |
| 津上S205A/S206A｜面板与基本操作 | `$tsugami-s20a-operation` | 17–23、56–86、137–141 |
| 津上S205A/S206A｜装刀与对芯 | `$tsugami-s20a-tooling` | 17–18、30–35、87–110、418–421 |
| 津上S205A/S206A｜程序编辑与数据备份 | `$tsugami-s20a-program-io` | 17–18、111–131、142–145、170–171 |
| 津上S205A/S206A｜坐标与刀具补正 | `$tsugami-s20a-offsets` | 17–18、87–90、132–136、148–150、247、273–276、302–310、314–317、330 |
| 津上S205A/S206A｜试运行与量产准备 | `$tsugami-s20a-production` | 17–26、164–188 |
| 津上S205A/S206A｜夹头与导套调整 | `$tsugami-s20a-workholding` | 17–18、194–229、399–407 |
| 津上S205A/S206A｜点检润滑与刀具寿命 | `$tsugami-s20a-maintenance` | 17–18、146–147、151–156、189–193、230–246 |
| 津上S205A/S206A｜原点电池与参数恢复 | `$tsugami-s20a-reference-recovery` | 17–18、124–131、247–261 |
| 津上S205A/S206A｜G代码与程序解读 | `$tsugami-s20a-programming` | 17–18、269–276、293–331 |
| 津上S205A/S206A｜M代码与双通道同步 | `$tsugami-s20a-m-codes-sync` | 17–23、157–163、259、277–292、328–331、345–350 |
| 津上S205A/S206A｜加工实例与切削条件 | `$tsugami-s20a-machining` | 17–18、293–295、312–313、328–366 |
| 津上S205A/S206A｜报警与故障排查 | `$tsugami-s20a-alarms` | 17–23、157–164、239–247、367–386 |
| 津上S205A/S206A｜选配附件 | `$tsugami-s20a-options` | 17–18、387–442 |
| 津上S205A/S206A｜电路图与信号追踪 | `$tsugami-s20a-electrical` | 17–18、443–485 |

## 跨模块分工

- 对刀、尺寸偏差与中心高：offsets；机械装刀/对芯：tooling；机器原点丢失：reference-recovery。
- G与坐标/模态：programming；M及双通道：m-codes-sync；完整加工实例：machining。
- 无法启动：先safety/alarms；日常检查：maintenance；实际电气连接：electrical。
- 选配是否适用：options；夹头导套的机械调整：workholding。
- 使用已发现技能的实际资源路径；安装后目录可能变成 skill-标识，需按 SKILL.md frontmatter 的 name 精确匹配调用名。不要假设调用名就是目录名。

## 原PDF逐页覆盖

| 原PDF页序 | 已核对/提取的纸面页码 | 主要模块 |
|---|---|---|
| 1 | 未提取/无可见页码 | manual |
| 2 | 未提取/无可见页码 | manual |
| 3 | 未提取/无可见页码 | manual |
| 4 | 未提取/无可见页码 | manual |
| 5 | 未提取/无可见页码 | manual |
| 6 | 未提取/无可见页码 | manual |
| 7 | 未提取/无可见页码 | manual |
| 8 | 未提取/无可见页码 | manual |
| 9 | 未提取/无可见页码 | manual |
| 10 | 未提取/无可见页码 | manual |
| 11 | 未提取/无可见页码 | manual |
| 12 | 未提取/无可见页码 | manual |
| 13 | 未提取/无可见页码 | manual |
| 14 | 未提取/无可见页码 | manual |
| 15 | 未提取/无可见页码 | manual |
| 16 | 未提取/无可见页码 | manual |
| 17 | 1-1 | manual, safety, installation, operation, tooling, program-io, offsets, production, workholding, maintenance, reference-recovery, programming, m-codes-sync, machining, alarms, options, electrical |
| 18 | 1-2 | manual, safety, installation, operation, tooling, program-io, offsets, production, workholding, maintenance, reference-recovery, programming, m-codes-sync, machining, alarms, options, electrical |
| 19 | 1-3 | safety, operation, production, m-codes-sync, alarms |
| 20 | 1-4 | safety, operation, production, m-codes-sync, alarms |
| 21 | 1-5 | safety, operation, production, m-codes-sync, alarms |
| 22 | 1-6 | safety, operation, production, m-codes-sync, alarms |
| 23 | 1-7 | safety, operation, production, m-codes-sync, alarms |
| 24 | 1-8 | safety, production |
| 25 | 1-9 | safety, production |
| 26 | 1-10 | safety, production |
| 27 | 2-1 | specifications |
| 28 | 2-2 | specifications |
| 29 | 2-3 | specifications |
| 30 | 2-4 | specifications, tooling |
| 31 | 2-5 | specifications, tooling |
| 32 | 2-6 | specifications, tooling |
| 33 | 2-7 | specifications, tooling |
| 34 | 2-8 | specifications, tooling |
| 35 | 2-9 | specifications, tooling |
| 36 | 2-10 | specifications |
| 37 | 2-11 | specifications |
| 38 | 2-12 | specifications |
| 39 | 2-13 | specifications |
| 40 | 2-14 | specifications |
| 41 | 2-15 | specifications |
| 42 | 2-16 | specifications |
| 43 | 2-17 | specifications |
| 44 | 2-18 | specifications |
| 45 | 2-19 | specifications |
| 46 | 2-20 | specifications |
| 47 | 2-21 | specifications |
| 48 | 2-22 | specifications |
| 49 | 3-1 | installation |
| 50 | 3-2 | installation |
| 51 | 3-3 | installation |
| 52 | 3-4 | installation |
| 53 | 3-5 | installation |
| 54 | 3-6 | installation |
| 55 | 3-7 | installation |
| 56 | 4-1 | safety, operation |
| 57 | 4-2 | operation |
| 58 | 4-3 | operation |
| 59 | 4-4 | operation |
| 60 | 4-5 | operation |
| 61 | 4-6 | operation |
| 62 | 4-7 | operation |
| 63 | 4-8 | operation |
| 64 | 4-9 | operation |
| 65 | 4-10 | operation |
| 66 | 4-11 | operation |
| 67 | 4-12 | operation |
| 68 | 4-13 | operation |
| 69 | 4-14 | operation |
| 70 | 4-15 | operation |
| 71 | 4-16 | operation |
| 72 | 4-17 | operation |
| 73 | 4-18 | operation |
| 74 | 4-19 | operation |
| 75 | 4-20 | operation |
| 76 | 4-21 | operation |
| 77 | 4-22 | operation |
| 78 | 4-23 | operation |
| 79 | 4-24 | operation |
| 80 | 4-25 | operation |
| 81 | 4-26 | operation |
| 82 | 4-27 | operation |
| 83 | 4-28 | operation |
| 84 | 4-29 | operation |
| 85 | 4-30 | operation |
| 86 | 4-31 | operation |
| 87 | 4-32 | tooling, offsets |
| 88 | 4-33 | tooling, offsets |
| 89 | 4-34 | tooling, offsets |
| 90 | 4-35 | tooling, offsets |
| 91 | 4-36 | tooling |
| 92 | 4-37 | tooling |
| 93 | 4-38 | tooling |
| 94 | 4-39 | tooling |
| 95 | 4-40 | tooling |
| 96 | 4-41 | tooling |
| 97 | 4-42 | tooling |
| 98 | 4-43 | tooling |
| 99 | 4-44 | tooling |
| 100 | 4-45 | tooling |
| 101 | 4-46 | tooling |
| 102 | 4-47 | tooling |
| 103 | 4-48 | tooling |
| 104 | 4-49 | tooling |
| 105 | 4-50 | tooling |
| 106 | 4-51 | tooling |
| 107 | 4-52 | tooling |
| 108 | 4-53 | tooling |
| 109 | 4-54 | tooling |
| 110 | 4-55 | tooling |
| 111 | 4-56 | program-io |
| 112 | 4-57 | program-io |
| 113 | 4-58 | program-io |
| 114 | 4-59 | program-io |
| 115 | 4-60 | program-io |
| 116 | 4-61 | program-io |
| 117 | 4-62 | program-io |
| 118 | 4-63 | program-io |
| 119 | 4-64 | program-io |
| 120 | 4-65 | program-io |
| 121 | 4-66 | program-io |
| 122 | 4-67 | program-io |
| 123 | 4-68 | program-io |
| 124 | 4-69 | program-io, reference-recovery |
| 125 | 4-70 | program-io, reference-recovery |
| 126 | 4-71 | program-io, reference-recovery |
| 127 | 4-72 | program-io, reference-recovery |
| 128 | 4-73 | program-io, reference-recovery |
| 129 | 4-74 | program-io, reference-recovery |
| 130 | 4-75 | program-io, reference-recovery |
| 131 | 4-76 | program-io, reference-recovery |
| 132 | 4-77 | offsets |
| 133 | 4-78 | offsets |
| 134 | 4-79 | offsets |
| 135 | 4-80 | offsets |
| 136 | 4-81 | offsets |
| 137 | 4-82 | operation |
| 138 | 4-83 | operation |
| 139 | 4-84 | operation |
| 140 | 4-85 | operation |
| 141 | 4-86 | operation |
| 142 | 4-87 | program-io |
| 143 | 4-88 | program-io |
| 144 | 4-89 | program-io |
| 145 | 4-90 | program-io |
| 146 | 4-91 | maintenance |
| 147 | 4-92 | maintenance |
| 148 | 4-93 | offsets |
| 149 | 4-94 | offsets |
| 150 | 4-95 | offsets |
| 151 | 4-96 | maintenance |
| 152 | 4-97 | maintenance |
| 153 | 4-98 | maintenance |
| 154 | 4-99 | maintenance |
| 155 | 4-100 | maintenance |
| 156 | 4-101 | maintenance |
| 157 | 4-102 | safety, m-codes-sync, alarms |
| 158 | 4-103 | safety, m-codes-sync, alarms |
| 159 | 4-104 | safety, m-codes-sync, alarms |
| 160 | 4-105 | safety, m-codes-sync, alarms |
| 161 | 4-106 | safety, m-codes-sync, alarms |
| 162 | 4-107 | safety, m-codes-sync, alarms |
| 163 | 4-108 | safety, m-codes-sync, alarms |
| 164 | 5-1 | safety, production, alarms |
| 165 | 5-2 | production |
| 166 | 5-3 | production |
| 167 | 5-4 | production |
| 168 | 5-5 | production |
| 169 | 5-6 | production |
| 170 | 5-7 | program-io, production |
| 171 | 5-8 | program-io, production |
| 172 | 5-9 | production |
| 173 | 5-10 | production |
| 174 | 5-11 | production |
| 175 | 5-12 | production |
| 176 | 5-13 | production |
| 177 | 5-14 | production |
| 178 | 5-15 | production |
| 179 | 5-16 | production |
| 180 | 5-17 | production |
| 181 | 5-18 | production |
| 182 | 5-19 | production |
| 183 | 5-20 | production |
| 184 | 5-21 | production |
| 185 | 5-22 | production |
| 186 | 5-23 | production |
| 187 | 5-24 | production |
| 188 | 5-25 | production |
| 189 | 6-1 | maintenance |
| 190 | 6-2 | maintenance |
| 191 | 6-3 | maintenance |
| 192 | 6-4 | maintenance |
| 193 | 6-5 | maintenance |
| 194 | 6-6 | workholding |
| 195 | 6-7 | workholding |
| 196 | 6-8 | workholding |
| 197 | 6-9 | workholding |
| 198 | 6-10 | workholding |
| 199 | 6-11 | workholding |
| 200 | 6-12 | workholding |
| 201 | 6-13 | workholding |
| 202 | 6-14 | workholding |
| 203 | 6-15 | workholding |
| 204 | 6-16 | workholding |
| 205 | 6-17 | workholding |
| 206 | 6-18 | workholding |
| 207 | 6-19 | workholding |
| 208 | 6-20 | workholding |
| 209 | 6-21 | workholding |
| 210 | 6-22 | workholding |
| 211 | 6-23 | workholding |
| 212 | 6-24 | workholding |
| 213 | 6-25 | workholding |
| 214 | 6-26 | workholding |
| 215 | 6-27 | workholding |
| 216 | 6-28 | workholding |
| 217 | 6-29 | workholding |
| 218 | 6-30 | workholding |
| 219 | 6-31 | workholding |
| 220 | 6-32 | workholding |
| 221 | 6-33 | workholding |
| 222 | 6-34 | workholding |
| 223 | 6-35 | workholding |
| 224 | 6-36 | workholding |
| 225 | 6-37 | workholding |
| 226 | 6-38 | workholding |
| 227 | 6-39 | workholding |
| 228 | 6-40 | workholding |
| 229 | 6-41 | workholding |
| 230 | 6-42 | maintenance |
| 231 | 6-43 | maintenance |
| 232 | 6-44 | maintenance |
| 233 | 6-45 | maintenance |
| 234 | 6-46 | maintenance |
| 235 | 6-47 | maintenance |
| 236 | 6-48 | maintenance |
| 237 | 6-49 | maintenance |
| 238 | 6-50 | maintenance |
| 239 | 6-51 | maintenance, alarms |
| 240 | 6-52 | maintenance, alarms |
| 241 | 6-53 | maintenance, alarms |
| 242 | 6-54 | maintenance, alarms |
| 243 | 6-55 | maintenance, alarms |
| 244 | 6-56 | maintenance, alarms |
| 245 | 6-57 | maintenance, alarms |
| 246 | 6-58 | maintenance, alarms |
| 247 | 6-59 | offsets, reference-recovery, alarms |
| 248 | 6-60 | reference-recovery |
| 249 | 6-61 | reference-recovery |
| 250 | 6-62 | reference-recovery |
| 251 | 6-63 | reference-recovery |
| 252 | 6-64 | reference-recovery |
| 253 | 6-65 | reference-recovery |
| 254 | 6-66 | reference-recovery |
| 255 | 6-67 | reference-recovery |
| 256 | 6-68 | reference-recovery |
| 257 | 6-69 | reference-recovery |
| 258 | 6-70 | reference-recovery |
| 259 | 6-71 | reference-recovery, m-codes-sync |
| 260 | 6-72 | reference-recovery |
| 261 | 6-73 | reference-recovery |
| 262 | 6-74 | specifications |
| 263 | 6-75 | specifications |
| 264 | 6-76 | specifications |
| 265 | 6-77 | specifications |
| 266 | 6-78 | specifications |
| 267 | 6-79 | specifications |
| 268 | 6-80 | specifications |
| 269 | 7-1 | programming |
| 270 | 7-2 | programming |
| 271 | 7-3 | programming |
| 272 | 7-4 | programming |
| 273 | 7-5 | offsets, programming |
| 274 | 7-6 | offsets, programming |
| 275 | 7-7 | offsets, programming |
| 276 | 7-8 | offsets, programming |
| 277 | 7-9 | m-codes-sync |
| 278 | 7-10 | m-codes-sync |
| 279 | 7-11 | m-codes-sync |
| 280 | 7-12 | m-codes-sync |
| 281 | 7-13 | m-codes-sync |
| 282 | 7-14 | m-codes-sync |
| 283 | 7-15 | m-codes-sync |
| 284 | 7-16 | m-codes-sync |
| 285 | 7-17 | m-codes-sync |
| 286 | 7-18 | m-codes-sync |
| 287 | 7-19 | m-codes-sync |
| 288 | 7-20 | m-codes-sync |
| 289 | 7-21 | m-codes-sync |
| 290 | 7-22 | m-codes-sync |
| 291 | 7-23 | m-codes-sync |
| 292 | 7-24 | m-codes-sync |
| 293 | 7-25 | programming, machining |
| 294 | 7-26 | programming, machining |
| 295 | 7-27 | programming, machining |
| 296 | 7-28 | programming |
| 297 | 7-29 | programming |
| 298 | 7-30 | programming |
| 299 | 7-31 | programming |
| 300 | 7-32 | programming |
| 301 | 7-33 | programming |
| 302 | 7-34 | offsets, programming |
| 303 | 7-35 | offsets, programming |
| 304 | 7-36 | offsets, programming |
| 305 | 7-37 | offsets, programming |
| 306 | 7-38 | offsets, programming |
| 307 | 7-39 | offsets, programming |
| 308 | 7-40 | offsets, programming |
| 309 | 7-41 | offsets, programming |
| 310 | 7-42 | offsets, programming |
| 311 | 7-43 | programming |
| 312 | 7-44 | programming, machining |
| 313 | 7-45 | programming, machining |
| 314 | 7-46 | offsets, programming |
| 315 | 7-47 | offsets, programming |
| 316 | 7-48 | offsets, programming |
| 317 | 7-49 | offsets, programming |
| 318 | 7-50 | programming |
| 319 | 7-51 | programming |
| 320 | 7-52 | programming |
| 321 | 7-53 | programming |
| 322 | 7-54 | programming |
| 323 | 7-55 | programming |
| 324 | 7-56 | programming |
| 325 | 7-57 | programming |
| 326 | 7-58 | programming |
| 327 | 7-59 | programming |
| 328 | 7-60 | programming, m-codes-sync, machining |
| 329 | 7-61 | programming, m-codes-sync, machining |
| 330 | 7-62 | offsets, programming, m-codes-sync, machining |
| 331 | 7-63 | programming, m-codes-sync, machining |
| 332 | 7-64 | machining |
| 333 | 7-65 | machining |
| 334 | 7-66 | machining |
| 335 | 7-67 | machining |
| 336 | 7-68 | machining |
| 337 | 7-69 | machining |
| 338 | 7-70 | machining |
| 339 | 7-71 | machining |
| 340 | 7-72 | machining |
| 341 | 7-73 | machining |
| 342 | 7-74 | machining |
| 343 | 7-75 | machining |
| 344 | 7-76 | machining |
| 345 | 7-77 | m-codes-sync, machining |
| 346 | 7-78 | m-codes-sync, machining |
| 347 | 7-79 | m-codes-sync, machining |
| 348 | 7-80 | m-codes-sync, machining |
| 349 | 7-81 | m-codes-sync, machining |
| 350 | 7-82 | m-codes-sync, machining |
| 351 | 7-83 | machining |
| 352 | 7-84 | machining |
| 353 | 7-85 | machining |
| 354 | 7-86 | machining |
| 355 | 7-87 | machining |
| 356 | 7-88 | machining |
| 357 | 7-89 | machining |
| 358 | 7-90 | machining |
| 359 | 7-91 | machining |
| 360 | 7-92 | machining |
| 361 | 7-93 | machining |
| 362 | 7-94 | machining |
| 363 | 未提取/无可见页码 | machining |
| 364 | 7-96 | machining |
| 365 | 7-97 | machining |
| 366 | 7-98 | machining |
| 367 | 8-1 | alarms |
| 368 | 8-2 | alarms |
| 369 | 8-3 | alarms |
| 370 | 8-4 | alarms |
| 371 | 8-5 | alarms |
| 372 | 8-6 | alarms |
| 373 | 8-7 | alarms |
| 374 | 8-8 | alarms |
| 375 | 8-9 | alarms |
| 376 | 8-10 | alarms |
| 377 | 8-11 | alarms |
| 378 | 8-12 | alarms |
| 379 | 8-13 | alarms |
| 380 | 8-14 | alarms |
| 381 | 8-15 | alarms |
| 382 | 8-16 | alarms |
| 383 | 8-17 | alarms |
| 384 | 8-18 | alarms |
| 385 | 8-19 | alarms |
| 386 | 8-20 | alarms |
| 387 | 9-1 | options |
| 388 | 9-2 | options |
| 389 | 9-3 | options |
| 390 | 9-4 | options |
| 391 | 9-5 | options |
| 392 | 9-6 | options |
| 393 | 9-7 | options |
| 394 | 9-8 | options |
| 395 | 9-9 | options |
| 396 | 9-10 | options |
| 397 | 9-11 | options |
| 398 | 9-12 | options |
| 399 | 9-13 | workholding, options |
| 400 | 9-14 | workholding, options |
| 401 | 9-15 | workholding, options |
| 402 | 9-16 | workholding, options |
| 403 | 9-17 | workholding, options |
| 404 | 9-18 | workholding, options |
| 405 | 9-19 | workholding, options |
| 406 | 9-20 | workholding, options |
| 407 | 9-21 | workholding, options |
| 408 | 9-22 | options |
| 409 | 9-23 | options |
| 410 | 9-24 | options |
| 411 | 9-25 | options |
| 412 | 9-26 | options |
| 413 | 9-27 | options |
| 414 | 9-28 | options |
| 415 | 9-29 | options |
| 416 | 9-30 | options |
| 417 | 9-31 | options |
| 418 | 9-32 | tooling, options |
| 419 | 9-33 | tooling, options |
| 420 | 9-34 | tooling, options |
| 421 | 9-35 | tooling, options |
| 422 | 9-36 | options |
| 423 | 9-37 | options |
| 424 | 9-38 | options |
| 425 | 9-39 | options |
| 426 | 9-40 | options |
| 427 | 9-41 | options |
| 428 | 9-42 | options |
| 429 | 9-43 | options |
| 430 | 9-44 | options |
| 431 | 9-45 | options |
| 432 | 9-46 | options |
| 433 | 9-47 | options |
| 434 | 9-48 | options |
| 435 | 9-49 | options |
| 436 | 9-50 | options |
| 437 | 9-51 | options |
| 438 | 9-52 | options |
| 439 | 9-53 | options |
| 440 | 9-54 | options |
| 441 | 9-55 | options |
| 442 | 9-56 | options |
| 443 | 3281-E310 图纸 1/42 | electrical |
| 444 | 3281-E310 图纸 2/42 | electrical |
| 445 | 3281-E310 图纸 3/42 | electrical |
| 446 | 3281-E310 图纸 4/42 | electrical |
| 447 | 3281-E310 图纸 5/42 | electrical |
| 448 | 3281-E310 图纸 6/42 | electrical |
| 449 | 3281-E310 图纸 7/42 | electrical |
| 450 | 3281-E310 图纸 8/42 | electrical |
| 451 | 3281-E310 图纸 9/42 | electrical |
| 452 | 3281-E310 图纸 10/42 | electrical |
| 453 | 3281-E310 图纸 11/42 | electrical |
| 454 | 3281-E310 图纸 12/42 | electrical |
| 455 | 3281-E310 图纸 13/42 | electrical |
| 456 | 3281-E310 图纸 14/42 | electrical |
| 457 | 3281-E310 图纸 15/42 | electrical |
| 458 | 3281-E310 图纸 16/42 | electrical |
| 459 | 3281-E310 图纸 17/42 | electrical |
| 460 | 3281-E310 图纸 18/42 | electrical |
| 461 | 3281-E310 图纸 19/42 | electrical |
| 462 | 3281-E310 图纸 20/42 | electrical |
| 463 | 3281-E310 图纸 21/42 | electrical |
| 464 | 3281-E310 图纸 22/42 | electrical |
| 465 | 3281-E310 图纸 23/42 | electrical |
| 466 | 3281-E310 图纸 24/42 | electrical |
| 467 | 3281-E310 图纸 25/42 | electrical |
| 468 | 3281-E310 图纸 26/42 | electrical |
| 469 | 3281-E310 图纸 27/42 | electrical |
| 470 | 3281-E310 图纸 28/42 | electrical |
| 471 | 3281-E310 图纸 29/42 | electrical |
| 472 | 3281-E310 图纸 30/42 | electrical |
| 473 | 3281-E310 图纸 31/42 | electrical |
| 474 | 3281-E310 图纸 32/42 | electrical |
| 475 | 3281-E310 图纸 33/42 | electrical |
| 476 | 3281-E310 图纸 34/42 | electrical |
| 477 | 3281-E310 图纸 35/42 | electrical |
| 478 | 3281-E310 图纸 36/42 | electrical |
| 479 | 3281-E310 图纸 37/42 | electrical |
| 480 | 3281-E310 图纸 38/42 | electrical |
| 481 | 3281-E310 图纸 39/42 | electrical |
| 482 | 3281-E310 图纸 40/42 | electrical |
| 483 | 3281-E310 图纸 41/42 | electrical |
| 484 | 3281-E310 图纸 42/42 | electrical |
| 485 | PMC标题资料 1 | electrical |
