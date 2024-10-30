# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : routes.py
# Time       ：2024/7/5 17:07
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
import os
import aiofiles
import json
import pandas as pd
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, \
    flash, jsonify, send_file, session
from werkzeug.security import generate_password_hash, check_password_hash
from agent.src.prompt import PromptSingleChat
from agent.utils import usr_system, requirements
from .forms import LoginForm, RegisterForm
from .utils import load_users, save_users, validate_username, validate_password, save_excel_to_json, \
    get_user_file_path,delete_remain_files
from agent.src.tool import BaseTool
from agent.utils import scene_tools_dict
from agent.src.llm import AppLLM
from data import check_agent_data, check_data_error, save_agent_data, transform_json_to_xlsx, \
    perform_analysis,transform_data,parse_chat_text,parse_save_data,readJsonLines
from .config import Config

DEFAULT_FILE = Config.DEFAULT_FILE
DEFAULT_FILE_JSON = Config.DEFAULT_FILE_JSON
project_dir = Config.PROJECT_DIR


class UserRoutes:
    def __init__(self, user_system):
        self.user_system = user_system
        self.page_size = 10
        self.bp = Blueprint('routes', __name__)
        self.bp.add_url_rule('/', view_func=self.index, methods=['GET'])
        self.bp.add_url_rule('/login', view_func=self.login, methods=['POST'])
        self.bp.add_url_rule('/logout', view_func=self.logout, methods=['POST'])
        self.bp.add_url_rule('/register', view_func=self.register, methods=['POST'])
        self.bp.add_url_rule('/dashboard', view_func=self.dashboard, methods=['GET'])
        self.bp.add_url_rule('/upload_data', view_func=self.upload_data, methods=['GET', 'POST'])
        self.bp.add_url_rule('/overview', view_func=self.overview, methods=['GET'])
        self.bp.add_url_rule('/data_overview', view_func=self.data_overview, methods=['POST'])
        self.bp.add_url_rule('/load', view_func=self.load_file, methods=['GET'])
        self.bp.add_url_rule('/export', view_func=self.export_file, methods=['GET'])
        self.bp.add_url_rule('/file_delete', view_func=self.delete_file, methods=['POST'])
        self.bp.add_url_rule('/data_preview', view_func=self.data_preview, methods=['GET'])
        self.bp.add_url_rule('/data', view_func=self.get_data, methods=['GET'])
        self.bp.add_url_rule('/restore/<int:item_id>', view_func=self.restore_data, methods=['POST'])
        self.bp.add_url_rule('/delete/<int:item_id>', view_func=self.delete_data, methods=['POST'])
        self.bp.add_url_rule('/online_annotation', view_func=self.online_annotation, methods=['GET'])
        self.bp.add_url_rule('/anno_data', view_func=self.get_anno_data, methods=['GET'])
        self.bp.add_url_rule('/anno_delete/<int:id>', view_func=self.delete_anno_item, methods=['POST'])
        self.bp.add_url_rule('/anno_restore/<int:id>', view_func=self.restore_anno_item, methods=['POST'])
        self.bp.add_url_rule('/inspect_data', view_func=self.inspect_data, methods=['POST'])
        self.bp.add_url_rule('/analyze_data', view_func=self.analyze_data, methods=['POST'])
        self.bp.add_url_rule('/save_anno_data', view_func=self.save_anno_data, methods=['POST'])
        self.bp.add_url_rule('/intelligent_analysis', view_func=self.intelligent_analysis, methods=['GET'])
        self.bp.add_url_rule('/analysis_data', view_func=self.get_analysis_data, methods=['GET'])
        self.bp.add_url_rule('/analysis_restore/<int:item_id>', view_func=self.restore_analysis_data, methods=['POST'])
        self.bp.add_url_rule('/analysis_delete/<int:item_id>', view_func=self.delete_analysis_data, methods=['POST'])
        self.bp.add_url_rule('/data_retrieval', view_func=self.data_retrieval, methods=['GET'])
        self.bp.add_url_rule('/data_retrieval_search', view_func=self.data_retrieval_search, methods=['POST'])
        self.bp.add_url_rule('/data_retrieval_replace', view_func=self.replace, methods=['POST'])
        self.bp.add_url_rule('/agent_call', view_func=self.agent_call, methods=['GET'])
        self.bp.add_url_rule('/call_tool', view_func=self.call_tool, methods=['POST'])
        self.bp.add_url_rule('/call_agent', view_func=self.call_agent, methods=['POST'])
        self.bp.add_url_rule('/generate_prompt', view_func=self.generate_prompt, methods=['POST'])
        self.bp.add_url_rule('/data_generation', view_func=self.data_generation, methods=['GET'])
        self.bp.add_url_rule('/agent_conversation', view_func=self.agent_conversation, methods=['GET'])
        self.bp.add_url_rule('/chat', view_func=self.chat_post, methods=['POST'])
        self.bp.add_url_rule('/delete_page', view_func=self.delete_page_data, methods=['POST'])
        self.bp.add_url_rule('/delete_all', view_func=self.delete_all_data, methods=['POST'])
        self.bp.add_url_rule('/restore_page', view_func=self.restore_page_data, methods=['POST'])
        self.bp.add_url_rule('/restore_all', view_func=self.restore_all_data, methods=['POST'])
        self.bp.add_url_rule('/delete_search_data/<int:id>', view_func=self.deleteSearchItem, methods=['POST'])
        self.bp.add_url_rule('/delete_all_search_data', view_func=self.delete_search_all_data, methods=['POST'])
        self.bp.add_url_rule('/data_process', view_func=self.data_process, methods=['GET'])
        self.bp.add_url_rule('/struct_data', view_func=self.get_struct_data, methods=['GET'])
        self.bp.add_url_rule('/view_processed_data', view_func=self.view_processed_data, methods=['POST'])
        self.bp.add_url_rule('/save_struct_data', view_func=self.save_struct_data, methods=['GET', 'POST'])
        self.bp.add_url_rule('/process_data_by_id', view_func=self.process_data_by_id, methods=['POST'])

    def index(self):
        login_form = LoginForm()
        register_form = RegisterForm()
        return render_template('index.html', login_form=login_form, register_form=register_form)

    def login(self):
        login_form = LoginForm()
        register_form = RegisterForm()
        users = load_users()

        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data
            if username in users and check_password_hash(users[username]['password'], password):
                flash('登录成功！', 'success')
                self.user_system.create_user_session(username)
                session['username'] = username

                user_folder = os.path.join(project_dir, 'datasets', 'user_uploads', username)
                user_excel_dir = os.path.join(project_dir, 'datasets', 'user_uploads', username, "excel_files")
                user_json_dir = os.path.join(project_dir, 'datasets', 'user_uploads', username, "json_files")
                os.makedirs(user_folder, exist_ok=True)
                os.makedirs(user_excel_dir, exist_ok=True)
                os.makedirs(user_json_dir, exist_ok=True)
                return redirect(url_for('routes.dashboard'))
            else:
                flash('未注册或者密码错误', 'error')
        return render_template('index.html', login_form=login_form, register_form=register_form)

    def logout(self):
        session.clear()
        return jsonify({'success': True}), 204

    def register(self):
        login_form = LoginForm()
        register_form = RegisterForm()
        users = load_users()

        if register_form.validate_on_submit():
            username = register_form.username.data
            password = register_form.password.data
            if not validate_username(username):
                flash('用户名长度必须在3到20之间', 'error')
            elif not validate_password(password):
                flash('密码长度必须在8到20之间', 'error')
            elif username not in users:
                hashed_password = generate_password_hash(password)
                users[username] = {'password': hashed_password}
                save_users(users)
                session['username'] = username
                user_folder = os.path.join(project_dir, 'datasets', 'user_uploads', username)
                user_excel_dir = os.path.join(project_dir, 'datasets', 'user_uploads', username, "excel_files")
                user_json_dir = os.path.join(project_dir, 'datasets', 'user_uploads', username, "json_files")
                os.makedirs(user_folder, exist_ok=True)
                os.makedirs(user_excel_dir, exist_ok=True)
                os.makedirs(user_json_dir, exist_ok=True)
                flash('注册成功！', 'success')
            else:
                flash('用户名已存在', 'error')
        return render_template('index.html', login_form=login_form, register_form=register_form)

    def dashboard(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        username = session['username']
        return render_template('dashboard.html', username=username)

    async def upload_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        if request.method == 'POST':
            file = request.files['file']
            dataset_name = request.form['dataset-name']
            dataset_type = request.form['dataset-type'] if request.form['dataset-type'] else "agent-split"
            dataset_version = request.form['dataset-version']

            if file and file.filename.endswith('.xlsx'):
                try:
                    df = pd.read_excel(file)
                    data_size = len(df)
                    if "is_annotated" in df.columns.tolist():
                        true_count = df['is_annotated'].sum()
                        anno_percent=str(true_count)
                    else:
                        anno_percent = "0"
                    upload_time = datetime.now().strftime('%Y%m%d%H%M%S')
                    new_filename = f"{dataset_version}_{dataset_name}_{dataset_type}_{upload_time}.xlsx"
                    file_path = os.path.join(user_session['user_excel_dir'], new_filename)
                    json_file = os.path.join(user_session['user_json_dir'], new_filename.replace(".xlsx", ".json"))
                    await delete_remain_files(user_session['user_excel_dir'],user_session['user_json_dir'])
                    code = save_excel_to_json(df, dataset_type,json_file)
                    if code == 0:
                        user_session['total'] = data_size
                        user_session['anno'] = int(anno_percent)
                        df.to_excel(file_path, index=False)
                        return jsonify({'status': 'success', 'message': '文件上传成功'}),200
                    elif code == -1:
                        return jsonify({'status': 'error', 'message': '必要字段缺失：问题和交互分开的Excel文件必须包含query和trajectory字段'}),501
                    elif code == -2:
                        return jsonify({'status': 'error', 'message': '必要字段缺失：问题和交互合并的Excel文件必须包含data字段'}),502
                    else:
                        return jsonify({'status': 'error', 'message': f'文件处理失败'}),503
                except Exception as e:
                    return jsonify({'status': 'error', 'message': f'文件处理失败: {e}'}),504
            else:
                return jsonify({'status': 'error', 'message': '仅支持.xlsx文件格式'}),505
        return render_template('upload_data.html', username=session['username'])

    def overview(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        return render_template('overview.html', username=session['username'])

    def data_overview(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        data_files = [f for f in os.listdir(user_session['user_excel_dir']) if f.endswith('.xlsx')]
        data_list = []
        user_excel_dir, user_json_dir = get_user_file_path(session["username"])

        for file in data_files:
            xlsx_file_path = os.path.abspath(os.path.join(user_excel_dir, file))
            json_name = file.replace("xlsx", "json")
            json_path = os.path.join(user_json_dir, json_name)
            if not os.path.exists(json_path):
                os.remove(xlsx_file_path)
                continue
            try:
                parts = file.split('_')
                version, data_name, data_type, upload_time = parts
                upload_time = upload_time.replace('.xlsx', '')
                data=readJsonLines(json_path)
                data_size=len(data)
                anno_percent=sum([1 if e["annotated"] else 0 for e in data])
                data_list.append({
                    'version': version,
                    'data_name': data_name,
                    'data_type': data_type,
                    'data_size': data_size,
                    'anno_percent': anno_percent,
                    'upload_time': upload_time,
                    'file_path': os.path.join(user_session['user_excel_dir'], file)
                })
            except Exception as e:
                print(f"Error processing file {file}: {e}")
                continue

        return jsonify(data_list)

    async def load_file(self):
        _, user_json_dir = get_user_file_path(session["username"])
        xlsx_file = request.args.get('file')
        xlsx_file = os.path.abspath(xlsx_file)
        file_name = os.path.basename(xlsx_file)
        name = file_name.replace(".xlsx", "").strip()

        if user_json_dir is not None and os.path.exists(user_json_dir) and name not in os.listdir(user_json_dir):
            json_name = name + ".json"
            json_file = os.path.abspath(os.path.join(user_json_dir, json_name))
            await check_agent_data(json_file)
        elif user_json_dir is not None and os.path.exists(user_json_dir) and name in os.listdir(user_json_dir):
            json_name = name + ".json"
            json_file = os.path.abspath(os.path.join(user_json_dir, json_name))
        else:
            return jsonify({'file_name': "未选择文件"})

        user_session = self.user_system.get_user_session(session['username'])
        user_session['user_xlsx_file'] = xlsx_file
        user_session['user_json_file'] = json_file
        print("load file:", json_file)
        await self.init_data(json_file)
        return jsonify({'file_name': file_name})

    async def export_file(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        user_session = self.user_system.get_user_session(session['username'])
        file_path = request.args.get('file', user_session['user_xlsx_file'])
        if os.path.exists(file_path):
            json_name = os.path.basename(file_path).replace("xlsx", "json")
            json_path = os.path.join(user_session['user_json_dir'], json_name)
            await transform_json_to_xlsx(json_path, file_path)
            return send_file(file_path, as_attachment=True,
                             mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        else:
            return jsonify({'error': 'File not found'}), 404

    async def delete_file(self):
        file_path = request.form['filePath']
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                file_path = os.path.abspath(file_path)
                cur_dir = os.path.dirname(file_path)
                parent_dir = os.path.dirname(cur_dir)
                json_path = os.path.join(parent_dir, "json_files",
                                         os.path.basename(file_path).replace(".xlsx", ".json"))
                if os.path.exists(json_path):
                    os.remove(json_path)
                xlsx_file_dir=os.path.join(parent_dir, "excel_files")
                json_file_dir=os.path.join(parent_dir, "json_files")
                await delete_remain_files(xlsx_file_dir,json_file_dir)
                return jsonify({"message": "文件已成功删除"}), 200
            else:
                return jsonify({"message": "文件不存在"}), 404
        except Exception as e:
            return jsonify({"message": "删除文件失败", "error": str(e)}), 500

    def data_preview(self):
        return render_template('data_preview.html', username=session['username'])

    async def get_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]

        if len(user_session["user_data"]) == 0:
            await self.load_data(user_session['user_json_file'])

        page = int(request.args.get('page', 1))
        filter_type = request.args.get('type', 'all')

        if filter_type == 'annotated':
            filtered_data = [item for item in data if
                             not item.get('is_delete', False) and item.get('annotated', False)]
        elif filter_type == 'unannotated':
            filtered_data = [item for item in data if
                             not item.get('is_delete', False) and not item.get('annotated', False)]
        elif filter_type == 'deleted':
            filtered_data = [item for item in data if item.get('is_delete', False)]
        else:
            filtered_data = [item for item in data if not item.get('is_delete', False)]

        start = (page - 1) * self.page_size
        end = start + self.page_size
        paginated_data = filtered_data[start:end]

        annotated_count = sum(
            1 for item in data if not item.get('is_delete', False) and item.get('annotated', False))
        unannotated_count = sum(
            1 for item in data if not item.get('is_delete', False) and not item.get('annotated', False))
        deleted_count = sum(1 for item in data if item.get('is_delete', False))
        total_count = len(data)

        user_session['total'] = total_count - deleted_count
        user_session['anno'] = annotated_count
        return jsonify({
            'data': paginated_data,
            'total': len(filtered_data),
            'annotated_count': annotated_count,
            'unannotated_count': unannotated_count,
            'deleted_count': deleted_count,
            'total_count': total_count,
            'page': page,
            'page_size': self.page_size
        })

    async def restore_data(self, item_id):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]
        for item in data:
            if item['id'] == item_id:
                item['is_delete'] = False
                break

        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return jsonify({'success': True})

    async def delete_page_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        user_session = self.user_system.get_user_session(session['username'])
        item_ids = request.json.get('ids', [])
        data = user_session['user_data']
        for item in data:
            if int(item['id']) in item_ids:
                item['is_delete'] = True
            else:
                continue
        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return '', 200

    async def delete_all_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]
        for item in data:
            item['is_delete'] = True
        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return '', 200

    async def restore_page_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]
        item_id = request.json.get('ids', [])

        for item in data:
            if int(item['id']) in item_id:
                item['is_delete'] = False
        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return '', 200

    async def restore_all_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]

        for item in data:
            item['is_delete'] = False
        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return '', 200

    async def delete_data(self, item_id):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]
        for item in data:
            if item['id'] == item_id:
                item['is_delete'] = True
                break
        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return jsonify({'success': True})

    async def online_annotation(self):
        return render_template('online_annotation.html', username=session['username'])

    async def get_anno_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]
        page = int(request.args.get('page', 1))
        page_size = 1
        data_type = request.args.get('type', 'all')

        if data_type == 'annotated':
            filtered_data = [item for item in data if
                             not item.get('is_delete', False) and item.get('annotated', False)]
        elif data_type == 'unannotated':
            filtered_data = [item for item in data if
                             not item.get('is_delete', False) and not item.get('annotated', False)]
        elif data_type == 'deleted':
            filtered_data = [item for item in data if item.get('is_delete', False)]
        elif data_type == "error":
            filtered_data = [item for item in data if
                             not item.get('is_delete', False) and item.get('error', False)]
        elif data_type == "correct":
            filtered_data = [item for item in data if
                             not item.get('is_delete', False) and not item.get('error', False)]
        else:
            filtered_data = [item for item in data if not item.get('is_delete', False)]

        total = len(filtered_data)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_data = filtered_data[start:end]

        annotated_count = sum(
            1 for item in data if not item.get('is_delete', False) and item.get('annotated', False))
        unannotated_count = sum(
            1 for item in data if not item.get('is_delete', False) and not item.get('annotated', False))
        deleted_count = sum(1 for item in data if item.get('is_delete', False))
        error_count = sum(1 for item in data if not item.get('is_delete', False) and item.get('error', False))
        correct_count = sum(
            1 for item in data if not item.get('is_delete', False) and not item.get('error', False))
        total_count = len(data)

        user_session['total'] = total_count - deleted_count
        user_session['anno'] = annotated_count
        return jsonify({
            'data': paginated_data,
            'total': total,
            'page_size': page_size,
            'total_count': total_count,
            'annotated_count': annotated_count,
            'unannotated_count': unannotated_count,
            'deleted_count': deleted_count,
            'error_count': error_count,
            'correct_count': correct_count
        })

    async def delete_anno_item(self, id):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]
        for item in data:
            if item['id'] == id:
                item['is_delete'] = True
                break
        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return jsonify({'success': True})

    async def deleteSearchItem(self, id):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]
        for item in data:
            if item['id'] == id:
                item['is_delete'] = True
                break
        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return jsonify({'success': True})

    async def delete_search_all_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]
        item_ids = request.json.get('ids', [])

        for item in data:
            if int(item['id']) in item_ids:
                item['is_delete'] = True
            else:
                continue
        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return jsonify({'success': True})

    async def restore_anno_item(self, id):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]
        for item in data:
            if item['id'] == id:
                item['is_delete'] = False
                break
        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return jsonify({'success': True})

    async def inspect_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        data = request.json
        data_id = data['id']
        text = data['text']
        user_session = self.user_system.get_user_session(session['username'])
        _, json_dir = get_user_file_path(session['username'])
        if user_session is not None and user_session['user_json_file'] != DEFAULT_FILE_JSON:
            json_file = os.path.join(json_dir, user_session['user_json_file'])
        else:
            json_file = DEFAULT_FILE_JSON
        msg = await check_data_error(json_file, data_id, text)
        return jsonify({'message': msg})

    def analyze_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        data = request.get_json()
        data_id = data.get('id')
        text = data.get('text')

        analysis_result = perform_analysis(data_id, text)
        return jsonify({'analysis': analysis_result})

    async def save_anno_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        data = request.json
        data_id = data['id']
        text = data['text']
        user_session = self.user_system.get_user_session(session['username'])
        _, json_dir = get_user_file_path(session['username'])
        if user_session is not None and user_session['user_json_file'] != DEFAULT_FILE_JSON:
            json_file = os.path.join(json_dir, user_session['user_json_file'])
        else:
            json_file = DEFAULT_FILE_JSON
        await save_agent_data(json_file, data_id, text)
        await self.load_data(json_file)
        return jsonify({'message': 'Data saved successfully'})

    def intelligent_analysis(self):
        return render_template('intelligent_analysis.html', username=session['username'])

    async def get_analysis_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        page = int(request.args.get('page', 1))
        filter_type = request.args.get('type', 'all')
        user_session = self.user_system.get_user_session(session['username'])
        data = user_session['user_data']

        if filter_type == 'correct_data':
            filtered_data = [item for item in data if
                             not item.get('is_delete', False) and not item.get('error', False)]
        elif filter_type == 'error_data':
            filtered_data = [item for item in data if
                             not item.get('is_delete', False) and item.get('error', False)]
        elif filter_type == 'deleted':
            filtered_data = [item for item in data if item.get('is_delete', False)]
        else:
            filtered_data = [item for item in data if not item.get('is_delete', False)]

        start = (page - 1) * self.page_size
        end = start + self.page_size
        paginated_data = filtered_data[start:end]

        correct_count = sum(
            1 for item in data if not item.get('is_delete', False) and not item.get('error', False))
        error_count = sum(1 for item in data if not item.get('is_delete', False) and item.get('error', False))
        deleted_count = sum(1 for item in data if item.get('is_delete', False))
        total_count = len(data)

        user_session['total'] = total_count - deleted_count
        return jsonify({
            'data': paginated_data,
            'total': len(filtered_data),
            'correct_count': correct_count,
            'error_count': error_count,
            'deleted_count': deleted_count,
            'total_count': total_count,
            'page': page,
            'page_size': self.page_size
        })

    async def restore_analysis_data(self, item_id):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        user_session = self.user_system.get_user_session(session['username'])
        data = user_session['user_data']
        for item in data:
            if item['id'] == item_id:
                item['is_delete'] = False
                break
        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return jsonify({'success': True})

    async def delete_analysis_data(self, item_id):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        user_session = self.user_system.get_user_session(session['username'])
        data = user_session['user_data']
        for item in data:
            if item['id'] == item_id:
                item['is_delete'] = True
                break
        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return jsonify({'success': True})

    def data_retrieval(self):
        return render_template('data_retrieval.html', username=session['username'])

    async def data_retrieval_search(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        text = request.json.get('text', '')
        user_session = self.user_system.get_user_session(session['username'])
        data = user_session['user_data']
        results = [item for item in data if text in item['text'] and not item["is_delete"]]
        return jsonify(results)

    async def replace(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        text1 = request.json.get('text1', '')
        text2 = request.json.get('text2', '')

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session['user_data']
        if not text1 or not text2:
            return jsonify({'success': False, 'message': '文本框1和文本框2不能为空', 'results': data})
        results = [item for item in data if text1 in item['text'] and not item["is_delete"]]

        replaced = False
        for item in results:
            item['text'] = item['text'].replace(text1, text2)
            replaced = True

        message = '替换成功' if replaced else '未找到匹配的文本内容'
        json_file = user_session["user_json_file"]
        await self.save_data(json_file)
        return jsonify({'success': replaced, 'message': message, 'results': results})

    def agent_call(self):
        return render_template('agent_call.html', username=session['username'])

    async def call_tool(self):
        data = request.json
        action = data.get('action')
        action_parameter = data.get('action_parameter')
        if isinstance(action_parameter, str):
            action_parameter = eval(action_parameter)

        try:
            observation, code = BaseTool.execute(action, **action_parameter)
            if code == 0:
                return jsonify(success=True, observation=observation)
            else:
                return jsonify(success=False, error="工具调用失败")
        except Exception as e:
            return jsonify(success=False, error=str(e))

    async def call_agent(self):
        data = request.get_json()
        input_text = data['input']
        llm_model = AppLLM()
        llm_input = input_text.strip()
        if "<ret>" not in llm_input:
            llm_input = llm_input.replace("\n", "<ret>")
        output_text = llm_model.chat(llm_input, is_remote=True)
        return jsonify({'output': output_text})

    async def generate_prompt(self):
        data = request.get_json()
        scene = data['scene']
        user_input = data['input']
        prompt = self.prompt_generation(scene, user_input)
        prompt = prompt.replace("<ret>", "\n")
        return jsonify({'prompt': prompt})

    def prompt_generation(self, scene, user_input):
        tool_lst = scene_tools_dict[scene]
        prompt = PromptSingleChat(usr_system, requirements).build_prompt_for_call(user_input, tool_lst)
        return prompt

    def data_generation(self):
        return render_template('data_generation.html', username=session['username'])

    def agent_conversation(self):
        return render_template('agent_conversation.html', username=session['username'])

    async def chat_post(self):
        data = request.get_json()
        message = data.get('message')
        reply = "这是一个示例回复：" + message
        return jsonify({'reply': reply})

    async def load_data(self, file_path):
        try:
            user_session = self.user_system.get_user_session(session['username'])
            user_session['user_data'] = []
            print(f"Reading JSON data from: {file_path}")

            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return

            async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
                async for line in f:
                    try:
                        user_session['user_data'].append(json.loads(line.strip()))
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")
                    except Exception as e:
                        print(f"Error reading line: {e}")

            print(f"Loaded {len(user_session['user_data'])} items from {file_path}")
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")


    async def save_data(self, file_path):
        try:
            user_session = self.user_system.get_user_session(session['username'])
            data = user_session['user_data']
            print(f"Saving JSON data to: {file_path}")

            async with aiofiles.open(file_path, mode='w', encoding='utf-8') as f:
                for item in data:
                    await f.write(json.dumps(item, ensure_ascii=False) + '\n')

            print(f"Saved {len(data)} items to {file_path}")
        except Exception as e:
            print(f"Error saving data to {file_path}: {e}")

    async def init_data(self, file_path=DEFAULT_FILE_JSON):
        print(f"Initializing data from: {file_path}")
        await self.load_data(file_path)

    def data_process(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        return render_template('data_process.html', username=session['username'])

    async def get_struct_data(self):
        if 'username' not in session:
            return redirect(url_for('routes.index'))

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]

        if len(user_session["user_data"]) == 0:
            await self.load_data(user_session['user_json_file'])

        page = int(request.args.get('page', 1))
        filter_type = request.args.get('type', 'all')

        if filter_type == 'annotated':
            filtered_data = [item for item in data if
                             not item.get('is_delete', False) and item.get('annotated', False)]
        elif filter_type == 'unannotated':
            filtered_data = [item for item in data if
                             not item.get('is_delete', False) and not item.get('annotated', False)]
        elif filter_type == 'deleted':
            filtered_data = [item for item in data if item.get('is_delete', False)]
        else:
            filtered_data = [item for item in data if not item.get('is_delete', False)]

        start = (page - 1) * 1
        end = start + 1
        paginated_data = filtered_data[start:end]

        annotated_count = sum(
            1 for item in data if not item.get('is_delete', False) and item.get('annotated', False))
        unannotated_count = sum(
            1 for item in data if not item.get('is_delete', False) and not item.get('annotated', False))
        deleted_count = sum(1 for item in data if item.get('is_delete', False))
        total_count = len(data)

        user_session['total'] = total_count - deleted_count
        user_session['anno'] = annotated_count
        return jsonify({
            'data': paginated_data,
            'total': len(filtered_data),
            'annotated_count': annotated_count,
            'unannotated_count': unannotated_count,
            'deleted_count': deleted_count,
            'total_count': total_count,
            'page': page,
            'page_size': 1
        })

    async def view_processed_data(self):
        if 'username' not in session:
            return jsonify({'error': '用户未登录'}), 401

        text =request.json.get('text',None)
        if text is not None:
            process_lst, code = parse_chat_text(text)
            if code == 0:
                current_data_json = transform_data(process_lst)
                return jsonify({"data": current_data_json})
            else:
                return jsonify({"error": "数据错误"})
        else:
            return jsonify({"error": "无数据"})


    async def save_struct_data(self):
        if 'username' not in session:
            return jsonify({'error': '用户未登录'}), 401

        text = request.json.get('data', None)
        id = request.json.get('page', None)
        if text is not None and id is not None:
            try:
                result, code = parse_save_data(text)
                if code == -1:
                    return jsonify({'error': f'数据处理失败!'}), 501

                if code != 0:
                    status = 500 + abs(code)
                    return jsonify({'error': result}), status

                data_id=int(id)
                user_session = self.user_system.get_user_session(session['username'])
                _, json_dir = get_user_file_path(session['username'])
                if user_session is not None and user_session['user_json_file'] != DEFAULT_FILE_JSON:
                    json_file = os.path.join(json_dir, user_session['user_json_file'])
                else:
                    json_file = DEFAULT_FILE_JSON
                await save_agent_data(json_file, data_id, result)
                await self.load_data(json_file)
                return jsonify({'success': '数据保存成功！'}), 200
            except Exception as e:
                return jsonify({'error': f'数据处理失败: {str(e)}'}), 500
        else:
            return jsonify({'error': '前端数据出错'}), 508


    async def process_data_by_id(self):
        if 'username' not in session:
            return jsonify({'error': '用户未登录'}), 401

        user_session = self.user_system.get_user_session(session['username'])
        data = user_session["user_data"]

        if len(user_session["user_data"]) == 0:
            await self.load_data(user_session['user_json_file'])

        index = int(request.form.get('index'))
        user_session = self.user_system.get_user_session(session['username'])
        _, json_dir = get_user_file_path(session['username'])
        if user_session is not None and user_session['user_json_file'] != DEFAULT_FILE_JSON:
            json_file = os.path.join(json_dir, user_session['user_json_file'])
        else:
            json_file = DEFAULT_FILE_JSON

        if not os.path.exists(json_file):
            return jsonify({'error': '没有找到文件'}), 404

        for item in data:
            if int(item['id']) == index:
                data=item
                break
        return jsonify({'data': data})


